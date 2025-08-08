// Publications data that can be shared between index.html and publications.html
const publicationsData = [
    {
        id: 3,
        title: "Robust Maritime Object Detection under Adverse Conditions via Joint Semantic Learning without Extra Computational Overhead",
        status: "Conference",
        venue: "The 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2025)",
        tldr: "Maritime Object Detection, Joint Semantic Learning",
        authors: "Junseok Lee, Seongju Lee, Jongwon Kim, Jumi Park, and Kyoobin Lee",
        type: "conference",
        selected: false
    },
    {
        id: 4,
        title: "MV2: A Novel Multi-View Maritime Vision Benchmark Dataset for Object Detection and Segmentation",
        status: "Conference",
        venue: "The 2025 IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2025)",
        tldr: "Multi-View Maritime Vision, Benchmark Dataset, Object Detection and Segmentation",
        authors: "Junseok Lee*, Jongwon Kim*, Seongju Lee*, Taeri Kim, and Kyoobin Lee",
        type: "conference",
        selected: true,
        paper: "https://drive.google.com/file/d/1e0xf1ej6gr0nOSYX_9NYVV-3A1DB3yBN/view?usp=sharing",
        website: "https://sites.google.com/view/multi-view-maritime-vision"
    },
    {
        id: 5,
        title: "MART: MultiscAle Relational Transformer Networks for Multi-agent Trajectory Prediction",
        status: "Top Conference",
        venue: "The 18th European Conference on Computer Vision (ECCV 2024), Poster",
        tldr: "Graph Neural Networks (GNNs), Hypergraph Transformer",
        authors: "Seongju Lee, Junseok Lee, Yeonguk Yu, Taeri Kim, and Kyoobin Lee",
        type: "top-conference",
        selected: true,
        paper: "https://link.springer.com/chapter/10.1007/978-3-031-72848-8_6",
        code: "https://github.com/gist-ailab/MART",
        acceptanceRate: "27.9%",
        citations: 16
    },
    {
        id: 6,
        title: "Block Selection Method for Using Feature Norm in Out-of-Distribution Detection",
        status: "Top Conference",
        venue: "2023 IEEE/CVF Computer Vision and Pattern Recognition Conference (CVPR 2023), Poster",
        tldr: "Out-of-Distribution Detection, Feature Norm, Block Selection",
        authors: "Yeonguk Yu, Sungho Shin, Seongju Lee, Changhyun Jun, and Kyoobin Lee",
        type: "top-conference",
        selected: false,
        paper: "https://openaccess.thecvf.com/content/CVPR2023/html/Yu_Block_Selection_Method_for_Using_Feature_Norm_in_Out-of-Distribution_Detection_CVPR_2023_paper.html",
        code: "https://github.com/gist-ailab/block-selection-for-OOD-detection",
        acceptanceRate: "25.8%",
        citations: 61
    },
    {
        id: 7,
        title: "SleePyCo: Automatic Sleep Scoring with Feature Pyramid and Contrastive Learning",
        status: "Journal",
        venue: "Expert Systems with Applications, 2024",
        tldr: "Automatic Sleep Scoring, Feature Pyramid, Contrastive Learning",
        authors: "Seongju Lee, Yeonguk Yu, Seunghyeok Back, Hogeon Seo, and Kyoobin Lee",
        type: "journal",
        selected: true,
        paper: "https://www.sciencedirect.com/science/article/pii/S0957417423030531",
        code: "https://github.com/gist-ailab/SleePyCo",
        impactFactor: "7.5 (Top 5.2%, Q1)",
        citations: 51
    },
    {
        id: 8,
        title: "BattleSound: A Game Sound Benchmark for the Sound-Specific Feedback Generation in a Battle Game",
        status: "Journal",
        venue: "Sensors, 2023",
        tldr: "Game Sound Benchmark, Sound-Specific Feedback, Battle Game",
        authors: "Sungho Shin, Seongju Lee, Changhyun Jun, and Kyoobin Lee",
        type: "journal",
        selected: false,
        paper: "https://www.mdpi.com/1424-8220/23/2/770",
        website: "https://sites.google.com/view/battlesound",
        impactFactor: "3.4 (Top 30.9%, Q2)",
        citations: 1
    },
    {
        id: 9,
        title: "Robust Skin Disease Classification by Distilling Deep Neural Network Ensemble for the Mobile Diagnosis of Herpes Zoster",
        status: "Journal",
        venue: "IEEE Access, 2021",
        tldr: "Skin Disease Classification, Deep Neural Network Ensemble, Mobile Diagnosis",
        authors: "Seunghyeok Back*, Seongju Lee*, Sungho Shin, Yeonguk Yu, Taekyeong Yuk, Saepomi Jong, Seungjun Ryu, Kyoobin Lee",
        type: "journal",
        selected: false,
        paper: "https://ieeexplore.ieee.org/abstract/document/9335582",
        impactFactor: "3.476 (Top 37.86%, Q2)",
        citations: 65
    },
    {
        id: 10,
        title: "Self-Supervised Transfer Learning from Natural Images for Sound Classification",
        status: "Journal",
        venue: "Applied Science, 2021",
        tldr: "Self-Supervised Learning, Transfer Learning, Sound Classification",
        authors: "Sungho Shin, Jongwon Kim, Yeonguk Yu, Seongju Lee, Kyoobin Lee",
        type: "journal",
        selected: false,
        paper: "https://www.mdpi.com/2076-3417/11/7/3043",
        impactFactor: "2.838 (Top 41.85%, Q2)",
        citations: 22
    },
    {
        id: 11,
        title: "Pilot study of a single-channel EEG seizure detection algorithm using machine learning",
        status: "Journal",
        venue: "Childs Nervous System, 2021",
        tldr: "EEG Seizure Detection, Machine Learning, Single-channel",
        authors: "Seungjun Ryu, Seunghyeok Back, Seongju Lee, Hyeon Seo, Chanki Park, Kyoobin Lee, Dong-Seok Kim",
        type: "journal",
        selected: false,
        paper: "https://link.springer.com/article/10.1007/s00381-020-05011-9",
        citations: 13
    },
    {
        id: 12,
        title: "Intra- and inter-epoch temporal context network (IITNet) using sub-epoch features for automatic sleep scoring on raw single-channel EEG",
        status: "Journal",
        venue: "Biomedical Signal Processing and Control, 2020",
        tldr: "IITNet, Temporal Context Network, Automatic Sleep Scoring",
        authors: "Hogeon Seo*, Seunghyeok Back*, Seongju Lee*, Deokhwan Park, Tae Kim, Kyoobin Lee",
        type: "journal",
        selected: false,
        paper: "https://www.sciencedirect.com/science/article/pii/S1746809420301932",
        code: "https://github.com/gist-ailab/IITNet-official",
        impactFactor: "3.88 (Top 37.64%, Q2)",
        citations: 242
    },
    {
        id: 13,
        title: "Buoy Light Detection and Pattern Classification for Unmanned Surface Vehicle Navigation",
        status: "Conference",
        venue: "The 21st International Conference on Ubiquitous Robots (UR 2024)",
        tldr: "Buoy Light Detection, Pattern Classification, USV Navigation",
        authors: "Junseok Lee, Taeri Kim, Seongju Lee, Jumi Park, and Kyoobin Lee",
        type: "conference",
        selected: false
    },
    {
        id: 14,
        title: "GYM-Net: Graphical Y-branched Multi-tasking Network for Trajectory Prediction",
        status: "Conference",
        venue: "The 22nd International Conference on Control, Automation and Systems (ICCAS 2022)",
        tldr: "Graphical Y-branched Network, Multi-tasking, Trajectory Prediction",
        authors: "Taeri Kim, Junseok Lee, Seongju Lee, and Kyoobin Lee",
        type: "conference",
        selected: false
    },
    {
        id: 15,
        title: "Vessel Trajectory Forecasting on Naval Warfare Simulation via CVAE-based Model",
        status: "Conference",
        venue: "The 9th International Conference on Robot Intelligence Technology and Applications (RiTA 2021)",
        tldr: "Vessel Trajectory Forecasting, CVAE-based Model, Naval Warfare Simulation",
        authors: "Seongju Lee*, Yeonguk Yu*, Junseok Lee, Jumi Park, Changhyun Jun, and Kyoobin Lee",
        type: "conference",
        selected: false
    },
    {
        id: 16,
        title: "Real-time Vibro-Acoustical Feedback for the Reality in Game by Detecting the Gun-Sound using Simple Convolutional Neural Network",
        status: "Conference",
        venue: "The 8th International Conference on Smart Media & Application (SMA 2019)",
        tldr: "Vibro-Acoustical Feedback, Gun-Sound Detection, Convolutional Neural Network",
        authors: "Sungho Shin, Seongju Lee, Changhyun Jeon, and Kyoobin Lee",
        type: "conference",
        selected: false
    }
];

// Function to get selected publications (MV2, MART, SleePyCo)
function getSelectedPublications() {
    return publicationsData.filter(publication => publication.selected);
}

// Function to get all publications
function getAllPublications() {
    return publicationsData;
}

// Function to get publications by type
function getPublicationsByType(type) {
    return publicationsData.filter(publication => publication.type === type);
} 