#include <math.h>
#include <stdio.h>

#include <cublas_v2.h>
#include <cuda_runtime.h>
#include <curand.h>
#include <thrust/binary_search.h>
#include <thrust/execution_policy.h>

#include "implicit/gpu/als.h"
#include "implicit/gpu/dot.cuh"
#include "implicit/gpu/utils.h"

namespace implicit {
namespace gpu {

__global__ void bpr_update_kernel(int samples, unsigned int *random_likes,
                                  unsigned int *random_dislikes, int *itemids,
                                  int *userids, int *indptr, size_t factors,
                                  float *X, float *Y, float learning_rate,
                                  float reg, bool verify_negative_samples,
                                  int *stats) {
  extern __shared__ float shared_memory[];
  float *temp = &shared_memory[0];

  int correct = 0, skipped = 0;

  for (int i = blockIdx.x; i < samples; i += gridDim.x) {
    int liked_index = random_likes[i] % samples,
        disliked_index = random_dislikes[i] % samples;

    int userid = userids[liked_index], likedid = itemids[liked_index],
        dislikedid = itemids[disliked_index];

    if (verify_negative_samples &&
        thrust::binary_search(thrust::seq, &itemids[indptr[userid]],
                              &itemids[indptr[userid + 1]], dislikedid)) {
      skipped += 1;
      continue;
    }

    float *user = &X[userid * factors], *liked = &Y[likedid * factors],
          *disliked = &Y[dislikedid * factors];

    float user_val = user[threadIdx.x], liked_val = liked[threadIdx.x],
          disliked_val = disliked[threadIdx.x];

    float score = dot(user_val, liked_val - disliked_val, temp);
    float z = 1.0 / (1.0 + exp(score));

    if (z < .5)
      correct++;

    liked[threadIdx.x] += learning_rate * (z * user_val - reg * liked_val);
    disliked[threadIdx.x] +=
        learning_rate * (-z * user_val - reg * disliked_val);

    // We're storing the item bias in the last column of the matrix - with the
    // user = 1 in that column. Don't update the user value in that case
    if (threadIdx.x < factors) {
      user[threadIdx.x] +=
          learning_rate * (z * (liked_val - disliked_val) - reg * user_val);
    }
  }

  if (threadIdx.x == 0) {
    atomicAdd(stats, correct);
    atomicAdd(stats + 1, skipped);
  }
}

std::pair<int, int> bpr_update(const Vector<int> &userids,
                               const Vector<int> &itemids,
                               const Vector<int> &indptr, Matrix *X, Matrix *Y,
                               float learning_rate, float reg, long seed,
                               bool verify_negative_samples) {
  if (X->cols != Y->cols)
    throw std::invalid_argument(
        "X and Y should have the same number of columns");
  if (userids.size != itemids.size)
    throw std::invalid_argument(
        "userids and itemids should have same number of elements");
  // todo: check indptr = X->rows + 1

  int nonzeros = userids.size;

  // allocate some memory
  int *stats;
  CHECK_CUDA(cudaMalloc(&stats, sizeof(int) * 2));
  CHECK_CUDA(cudaMemset(stats, 0, sizeof(int) * 2));

  // initialize memory for randomly picked positive/negative items
  unsigned int *random_likes, *random_dislikes;
  CHECK_CUDA(cudaMalloc(&random_likes, nonzeros * sizeof(unsigned int)));
  CHECK_CUDA(cudaMalloc(&random_dislikes, nonzeros * sizeof(unsigned int)));

  // Create a seeded RNG
  curandGenerator_t rng;
  CHECK_CURAND(curandCreateGenerator(&rng, CURAND_RNG_PSEUDO_DEFAULT));
  CHECK_CURAND(curandSetPseudoRandomGeneratorSeed(rng, seed));

  // Randomly pick values
  CHECK_CURAND(curandGenerate(rng, random_likes, nonzeros));
  CHECK_CURAND(curandGenerate(rng, random_dislikes, nonzeros));

  // TODO: multi-gpu support
  int devId;
  CHECK_CUDA(cudaGetDevice(&devId));

  int multiprocessor_count;
  CHECK_CUDA(cudaDeviceGetAttribute(&multiprocessor_count,
                                    cudaDevAttrMultiProcessorCount, devId));

  int factors = X->cols;
  int block_count = 256 * multiprocessor_count;
  int thread_count = factors;
  int shared_memory_size = sizeof(float) * (factors);

  // TODO: get rows passed in here
  bpr_update_kernel<<<block_count, thread_count, shared_memory_size>>>(
      nonzeros, random_likes, random_dislikes, itemids.data, userids.data,
      indptr.data, factors, X->data, Y->data, learning_rate, reg,
      verify_negative_samples, stats);

  CHECK_CUDA(cudaDeviceSynchronize());

  // we're returning the number of correctly ranked items, get that value from
  // the device
  int output[2];
  CHECK_CUDA(
      cudaMemcpy(output, stats, 2 * sizeof(int), cudaMemcpyDeviceToHost));

  CHECK_CUDA(cudaFree(random_likes));
  CHECK_CUDA(cudaFree(random_dislikes));
  CHECK_CUDA(cudaFree(stats));
  curandDestroyGenerator(rng);
  return std::make_pair(output[0], output[1]);
}
} // namespace gpu
} // namespace implicit
