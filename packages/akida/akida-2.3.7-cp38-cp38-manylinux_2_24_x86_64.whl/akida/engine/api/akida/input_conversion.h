#pragma once

#include <cstdint>

#include "akida/dense.h"
#include "akida/sparse.h"

#include "infra/exports.h"

namespace akida {

namespace conversion {

AKIDASHAREDLIB_EXPORT
const Sparse* as_sparse(const Tensor& input);

AKIDASHAREDLIB_EXPORT
SparseUniquePtr to_sparse(const Dense& input, const uint8_t* program);

AKIDASHAREDLIB_EXPORT
const Dense* as_dense(const Tensor& input);

AKIDASHAREDLIB_EXPORT
DenseUniquePtr to_dense(const Sparse& input);

AKIDASHAREDLIB_EXPORT
bool dense_input_expected(const uint8_t* program);

}  // namespace conversion
}  // namespace akida
