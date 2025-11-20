"""
usage:
    python batch_predict.py -r pegRNA_tail.fa -p uniprotkb_go_0008266_AND_ft_domain_HTH_2025_11_18.fasta -o Result
 
"""

import os
import subprocess
import argparse
from Bio import SeqIO

def main():
    parser = argparse.ArgumentParser(description="Batch predict RNA-protein interaction")
    parser.add_argument("-r", "--RNA_fasta", required=True, help="Single RNA fasta file")
    parser.add_argument("-p", "--protein_fasta", required=True, help="Protein FASTA file (multiple sequences)")
    parser.add_argument("-o", "--output_dir", required=True, help="Output directory")
    parser.add_argument("--script", default="predict_RPI_modified.py", help="Path to predict_RPI.py script")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    # --- 获取 RNA 名 ---
    rna_record = next(SeqIO.parse(args.RNA_fasta, "fasta"))
    rna_name = rna_record.id

    # --- 遍历蛋白序列 ---
    for prot_record in SeqIO.parse(args.protein_fasta, "fasta"):
        prot_name = prot_record.id

        # 为每条序列生成一个临时 fasta 文件
        tmp_prot_fasta = f"tmp_{prot_name}.fasta"
        with open(tmp_prot_fasta, "w") as f:
            f.write(f">{prot_record.id}\n{str(prot_record.seq)}\n")

        # 结果文件名：RNAID-ProteinID.txt
        jobname = f"{rna_name}-{prot_name}"

        # 调用原 predict_RPI.py
        cmd = [
            "python", args.script,
            "-r", args.RNA_fasta,
            "-p", tmp_prot_fasta,
            "-j", jobname,
            "-o", args.output_dir
        ]

        print(f"Running prediction for {prot_name} ...")
        subprocess.run(cmd)

        # 删除临时文件
        os.remove(tmp_prot_fasta)

    print("\n全部蛋白序列预测完成！")

if __name__ == "__main__":
    main()

