# Co-conservation
## Co-conservation analysis of sequence pairs
Sequence pairs co-conservation analysis. The input files are clustered **.tsv
files** of both sequence_1 and sequence_2. The output will be monolayer SSNs of
sequence_1 and _2 and a multilayer SSN that connects sequence pairs
```
optional arguments:
  -h, --help            show this help message and exit
  -seq1 SEQ1_PATH, --seq1_path SEQ1_PATH
                        <-seq1 /home/seq1.tsv> The first .tsv file generated
                        by mmseq2
  -seq2 SEQ2_PATH, --seq2_path SEQ2_PATH
                        <-seq2 /home/seq2.tsv> The second .tsv file generated
                        by mmseq2
  -seq1_node_num SEQ1_NODE_NUM, --seq1_node_num SEQ1_NODE_NUM
                        <--seq1_node_num 3> The minimal node number in a
                        cluster for seq1
  -seq2_node_num SEQ2_NODE_NUM, --seq2_node_num SEQ2_NODE_NUM
                        <--seq2_node_num 3> The minimal node number in a
                        cluster for seq2
  -c COVERAGE, --coverage COVERAGE
                        <--coverage 0.3> coverage = (seq1∩seq2)/seq2
  -o OUTDIR, --outdir OUTDIR
                        <-o /test/output> A path to save output files. e.g.,
                        ./output
```
Reproduce the unedited Figure 1B in this paper: [Bacterial Cytochrome P450-catalyzed Post-translational Macrocyclization](https://www.biorxiv.org/content/10.1101/2023.05.08.539676v1.article-metrics)
```
python pre2enzyme_layer_arg.py -seq1 "/data/bbhe/0-p450_pub_figure/figure_2/pre_0.35_out_cluster.tsv" -seq2 "/data/bbhe/0-p450_pub_figure/figure_2/P450_0.60_out_cluster.tsv" -seq1_node_num 0 -seq2_node_num 0 -c 0.3 -o /data/bbhe/txt_process/test_mssn
```
The input .tsv files can be found at 
```
/input_tsv
```
The output will be three figures:
```
/output
pre_0.35_out_cluster_SSN.png
P450_0.60_out_cluster_SSN.png
seq_pairs_SSN.svg
```
**pre_0.35_out_cluster_SSN.png**
![pre_0_SSN](https://github.com/Bio-bbhe/co-conservation/assets/82441159/c5d7c4fd-081c-4c5d-9eb3-a9e072dcdf8f)
**P450_0.60_out_cluster_SSN.png**
![P450_0_SSN](https://github.com/Bio-bbhe/co-conservation/assets/82441159/6418497c-5fc0-43f3-92ba-85419822dd8a)
**seq_pairs_SSN** which is the unedited version of Figure 1B in our paper: [Bacterial Cytochrome P450-catalyzed Post-translational Macrocyclization](https://www.biorxiv.org/content/10.1101/2023.05.08.539676v1.article-metrics)
![seq_pairs_SSN](https://github.com/Bio-bbhe/co-conservation/assets/82441159/d7561c4a-feed-41c1-8d91-5b5d4fc3ffa4)

