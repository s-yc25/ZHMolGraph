#用法：python extract_scores.py 目录 scores.tsv
#接下来sort：sort -k2,2nr Result/scores.txt > sorted.tsv


import os
import sys
import re

def extract_probability(filepath):
    """从文件中提取 Probability score"""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # 例子：Probability score: 0.220
    match = re.search(r"Probability score:\s*([0-9.]+)", text)
    if match:
        return match.group(1)
    return None


def main(input_folder, output_file):
    results = []

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(input_folder, filename)
            score = extract_probability(filepath)
            results.append((filename, score if score is not None else "NA"))

    # 写输出文件
    with open(output_file, "w", encoding="utf-8") as out:
        out.write("filename\tprobability_score\n")
        for filename, score in results:
            out.write(f"{filename}\t{score}\n")

    print(f"Done! Results saved to: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_scores.py <input_folder> <output_file>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_file = sys.argv[2]
    main(input_folder, output_file)

