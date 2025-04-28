import pandas as pd
from datetime import datetime
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity
from modules.embedding_service import get_embedding
from modules.cache_manager import load_cache, save_cache
from setup_logger import logger
from config import SIMILARITY_THRESHOLD
from openai import OpenAI
import tiktoken

encoder = tiktoken.encoding_for_model("text-embedding-ada-002")

def find_duplicates_among_issues(issues):
    cache = load_cache()

    embeddings = []
    keys = []
    full_texts = []
    summaries = []

    embedding_calls = 0
    total_input_length = 0
    total_tokens = 0

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
        full_texts.append(full_text)
        summaries.append(full_text.split("\n")[0])

    save_cache(cache)

    logger.info("[INFO] 이슈 간 유사도 계산 중...")

    similarities = cosine_similarity(embeddings)
    n = len(keys)

    printed_pairs = []
    result_lines = []

    for i in range(n):
        for j in range(i + 1, n):
            if similarities[i][j] >= SIMILARITY_THRESHOLD:
                printed_pairs.append((keys[i], keys[j], similarities[i][j], summaries[i], summaries[j]))
                line = f"- [{keys[i]}] {summaries[i]} ↔ [{keys[j]}] {summaries[j]} (유사도: {similarities[i][j]:.2f})"
                logger.info(line)
                result_lines.append(line)

    logger.info("\n[INFO] 총 %d개의 유사 이슈 쌍을 발견했습니다.", len(result_lines))

    save_results_to_excel(printed_pairs)

    logger.info("\n\n[AI 사용량 요약]")
    logger.info("- Embedding API 요청 수: %d회", embedding_calls)
    logger.info("- 총 Input 길이 (문자 수): %d자", total_input_length)
    logger.info("- 총 Input 토큰 수: %d tokens", total_tokens)
    estimated_cost = (total_tokens / 1000) * 0.0001
    logger.info("- 예상 Embedding 비용: ${:.6f}".format(estimated_cost))

def save_results_to_excel(pairs):
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame([
        {
            "Left Issue Key": left,
            "Left Issue Summary": left_summary,
            "Right Issue Key": right,
            "Right Issue Summary": right_summary,
            "Similarity": f"{similarity:.2f}"
        }
        for (left, right, similarity, left_summary, right_summary) in pairs
    ])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"duplicate_issues_result_{timestamp}.xlsx")
    df.to_excel(output_file, index=False)

    logger.info("\n[INFO] 엑셀 파일 저장 완료: %s", output_file)
