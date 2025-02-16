# Elikas RUST

## TODO

- 동작 검증
  - 1차 테스트 결과 unknown만 나옴. wasm 자체가 동작하는지 여부부터 확인해봐얄 듯(by using log?)
- 최적화: Rust 언어 관점에서(not biz logic)

## Getting started

1. Rust 설치. 참고로 macOS에서 brew로 설치하면 정상 compile안됨. 따라서 Rust 공식 설치 Path를 따라야.
   - `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. target 설치: `rustup target add wasm32-unknown-unknown`
3. build: `cargo build --target wasm32-unknown-unknown --release`
4. oci registry에 등록: `./wasm-to-oci push target/wasm32-unknown-unknown/release/openapi_path_filter.wasm docker-registry.anyflow.net/api-signature-filter:0.1.0`
   - `wasm-to-oci`는 `./`에 위치. `chmod +x` 해줘야.
     - 출처: `https://arc.net/l/quote/zbnovlje`. https://github.com/engineerd/wasm-to-oci/releases 참고
   - macOS에서는 security 건으로 실행을 막음. Settings - Security에서 허용을 해줘야 실행 가능
5. `curl -X GET https://docker-registry.anyflow.net/v2/_catalog` 를 통해 정상 등록되었는지 확인