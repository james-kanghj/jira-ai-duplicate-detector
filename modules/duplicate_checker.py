import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from modules.embedding_service import get_embedding
from modules.cache_manager import load_cache, save_cache
import tiktoken

def find_duplicates_among_issues(issues, logger, threshold=0.99):
    cache = load_cache()

    embeddings = []
    keys = []
    summaries = []

    embedding_calls = 0
    total_input_length = 0
    total_tokens = 0

    encoder = tiktoken.encoding_for_model("text-embedding-ada-002")

    logger.info("[INFO] 이슈 임베딩 로딩 또는 생성 중...")
    for key, full_text in issues:
        if key in cache:
            emb = np.array(cache[key])
        else:
            emb = get_embedding(full_text)
            cache[key] = emb.tolist()
            embedding_calls += 1
            total_input_length += len(full_text)
            total_tokens += len(encoder.encode(full_text))

        embeddings.append(np.array(cache[key]))
        keys.append(key)
        summaries.append(full_text.split("\n")[0])

    save_cache(cache)

    embeddings = np.vstack(embeddings)

    logger.info("[INFO] 이슈 간 유사도 계산 중...")
    similarity_matrix = cosine_similarity(embeddings)

    logger.info("\n[유사도 결과 (유사도 {:.2f} 이상)]".format(threshold))
    n = len(keys)
    found_duplicates = 0

    for i in range(n):
        left_key = keys[i]
        left_summary = summaries[i]

        for j in range(i + 1, n):
            right_key = keys[j]
            right_summary = summaries[j]

            similarity = similarity_matrix[i, j]

            if similarity >= threshold:
                found_duplicates += 1
                logger.info(
                    f"- [{left_key}] {left_summary} ↔ [{right_key}] {right_summary} (유사도: {similarity:.2f})"
                )

    if found_duplicates == 0:
        logger.info("\n[INFO] 유사한 이슈를 찾지 못했습니다.")
    else:
        logger.info(f"\n[INFO] 총 {found_duplicates}개의 유사 이슈 쌍을 발견했습니다.")

    logger.info("\n\n[AI 사용량 요약]")
    logger.info(f"- Embedding API 요청 수: {embedding_calls}회")
    logger.info(f"- 총 Input 길이 (문자 수 기준): {total_input_length}자")
    logger.info(f"- 총 Input 토큰 수: {total_tokens} tokens")
    estimated_cost = (total_tokens / 1000) * 0.0001
    logger.info(f"- 예상 Embedding 비용: ${estimated_cost:.6f}")
