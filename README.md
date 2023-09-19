# Abtract
This paper presents VulnSense framework, a comprehensive approach to efficiently detect vulnerabilities in Ethereum smart con-
tracts using a multimodal learning approach on graph-based and natural language processing (NLP) models. Our proposed frame-
work combines three types of features from smart contracts comprising source code, opcode sequences, and control flow graph
(CFG) extracted from bytecode. We employ Bidirectional Encoder Representations from Transformers (BERT), Bidirectional Long
Short-Term Memory (BiLSTM) and Graph Neural Network (GNN) models to extract and analyze these features. The final layer of
our multimodal approach consists of a fully connected layer used to predict vulnerabilities in Ethereum smart contracts. Address-
ing limitations of existing vulnerability detection methods relying on single-feature or single-model deep learning techniques, our
method surpasses accuracy and effectiveness constraints. We assess VulnSense using a collection of 1.769 smart contracts derived
from the combination of three datasets: Curated, SolidiFI-Benchmark, and Smartbugs Wild. We then make a comparison with
various unimodal and multimodal learning techniques contributed by GNN, BiLSTM and BERT architectures. The experimental
outcomes demonstrate the superior performance of our proposed approach, achieving an average accuracy of 77.96% across all
three categories of vulnerable smart contracts.

# Multimodal in VulnSense Framework
![VulnSense Framework](images/Multimodal_Vulnsense.jpg)
 
