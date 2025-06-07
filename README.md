

# MCIP: Protecting MCP Safety via Model Contextual Integrity Protocol

[Huihao Jing](https://egbertjing.github.io/)<sup>1</sup>, 
[Haoran Li](https://hlibt.student.ust.hk/)<sup>🤗 1</sup>, 
[Wenbin Hu](https://whuak.github.io/)<sup>1</sup>, 
Qi Hu<sup>1</sup>, 
Heli Xu<sup>2</sup>
Tianshu Chu<sup>2</sup>, 
[Peizhao Hu](https://www.cs.rit.edu/~ph/)<sup>2</sup>, 
[Yangqiu Song](https://www.cse.ust.hk/~yqsong/)<sup>1</sup>

<sup>🤗</sup>Corresponding author.

<sup>1</sup>Hong Kong University of Science and Technology, 
<sup>2</sup>HuaweiTechnologies


<p align="center">
  <a href='https://arxiv.org/abs/2505.14590'>
  <img src='https://img.shields.io/badge/Arxiv-2405.20340-A42C25?style=flat&logo=arXiv&logoColor=A42C25'>
  </a> 
  <a href='https://arxiv.org/pdf/2505.14590.pdf'>
  <img src='https://img.shields.io/badge/Paper-PDF-yellow?style=flat&logo=arXiv&logoColor=yellow'>
  </a> 
<!--   <a href='https://lhchen.top/MotionLLM'>
  <img src='https://img.shields.io/badge/Project-Page-%23df5b46?style=flat&logo=Google%20chrome&logoColor=%23df5b46'></a>  -->
<!--   <a href='https://research.lhchen.top/blogpost/motionllm'>
    <img src='https://img.shields.io/badge/Blog-post-4EABE6?style=flat&logoColor=4EABE6'></a> -->
  <a href='https://github.com/HKUST-KnowComp/MCIP'>
  <img src='https://img.shields.io/badge/GitHub-Code-black?style=flat&logo=github&logoColor=white'></a> 
  <a href='LICENSE'>
  <img src='https://img.shields.io/badge/License-IDEA-blue.svg'>
  </a> 
  <a href="" target='_blank'>
  <img src="https://visitor-badge.laobi.icu/badge?page_id=HKUST-KnowComp.MCIP&left_color=gray&right_color=%2342b983">
  </a> 
</p>

# 🤩 Abstract

As Model Context Protocol (MCP) introduces an easy-to-use ecosystem for users and developers, it also brings underexplored safety risks. Its decentralized architecture, which separates clients and servers, poses unique challenges for systematic safety analysis. This paper proposes a novel framework to enhance MCP safety. Guided by the MAESTRO framework, we first analyze the missing safety mechanisms in MCP, and based on this analysis, we propose the Model Contextual Integrity Protocol (MCIP), a refined version of MCP that addresses these gaps. 
Next, we develop a fine-grained taxonomy that captures a diverse range of unsafe behaviors observed in MCP scenarios.  Building on this taxonomy, we develop benchmark and training data that support the evaluation and improvement of LLMs' capabilities in identifying safety risks within MCP interactions. Leveraging the proposed benchmark and training data, we conduct extensive experiments on state-of-the-art LLMs. The results highlight LLMs' vulnerabilities in MCP interactions and demonstrate that our approach substantially improves their safety performance.

# 😎 Our Contributions
## Safety Analysis to MCP
![application](./assets/application.png)




# Quick Start: try our MCIP Guardian
```
bash dp_eval.sh
```

# Citation
Please kindly cite the following paper if you found our method and resources helpful!
```
@misc{jing2025mcipprotectingmcpsafety,
      title={MCIP: Protecting MCP Safety via Model Contextual Integrity Protocol}, 
      author={Huihao Jing and Haoran Li and Wenbin Hu and Qi Hu and Heli Xu and Tianshu Chu and Peizhao Hu and Yangqiu Song},
      year={2025},
      eprint={2505.14590},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2505.14590}, 
}
```
# Miscellaneous
Please send any questions about the code and/or the method to hjingaa@connect.ust.hk
<div align="center">

<pre>
███╗   ███╗ ██████╗ ██╗██████╗ 
████╗ ████║██╔════╝ ██║██╔══██╗
██╔████╔██║██║      ██║██████╔╝
██║╚██╔╝██║██║      ██║██╔═══╝ 
██║ ╚═╝ ██║╚██████╗ ██║██║     
╚═╝     ╚═╝ ╚═════╝ ╚═╝╚═╝  
</pre>

</div>
