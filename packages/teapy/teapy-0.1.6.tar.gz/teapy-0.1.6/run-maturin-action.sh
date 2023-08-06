#!/bin/bash
set -e
echo "::group::Install Rust"
which rustup > /dev/null || curl --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain nightly-2023-06-01
export PATH="$HOME/.cargo/bin:$PATH"
rustup override set nightly-2023-06-01
rustup component add llvm-tools-preview || true
echo "::endgroup::"
export PATH="$PATH:/opt/python/cp37-cp37m/bin:/opt/python/cp38-cp38/bin:/opt/python/cp39-cp39/bin:/opt/python/cp310-cp310/bin:/opt/python/cp311-cp311/bin"
echo "::group::Install maturin"
curl -L https://github.com/PyO3/maturin/releases/download/v1.0.1/maturin-x86_64-unknown-linux-musl.tar.gz | tar -xz -C /usr/local/bin
maturin --version || true
which patchelf > /dev/null || python3 -m pip install patchelf
python3 -m pip install cffi || true
echo "::endgroup::"
maturin publish --skip-existing -o wheels -u teamon