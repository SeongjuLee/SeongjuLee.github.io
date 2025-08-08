// Projects data that can be shared between index.html and projects.html
const projectsData = [
    {
        id: 1,
        title: "Development of Humanoid Robots that Feel Like Humans, Communicate, and Grow through Learning",
        shortTitle: "Alchemist Project",
        period: "May 2025 -- Present",
        organization: "Ministry of Trade, Industry and Energy (MOTIE), South Korea",
        role: "AI Developer",
        tldr: "Development of Physical Reasoning Pretrained Model",
        icon: "bot",
        gradient: "from-indigo-500 to-purple-600",
        tags: ["Physical Reasoning", "Pretrained Model", "MOTIE"],
        featured: true
    },
    {
        id: 2,
        title: "Development of Micro Intelligent Drone for Autonomous Mission in Communication/GPS-denied Environments",
        shortTitle: "Micro Intelligent Drone",
        period: "Sep. 2023 -- Present",
        organization: "Institute of Civil-Military Technology Cooperation (ICMTC), South Korea",
        role: "Project Member, Software Developer",
        tldr: "Development of an RGB-IR-Based Object Detection Model and Construction of a Multi-Modal Database Including RGB, IR, and LiDAR Captured from Drone Views",
        icon: "drone",
        gradient: "from-teal-500 to-cyan-600",
        tags: ["Object Detection", "Multi-Modal", "ICMTC"],
        featured: true
    },
    {
        id: 3,
        title: "Development of a Situational Awareness System for Preventing Collisions and Accidents of Autonomous Ship",
        shortTitle: "Autonomous Ship Project",
        period: "Apr. 2023 -- Dec. 2024",
        organization: "Ministry of Trade, Industry and Energy (MOTIE), South Korea",
        role: "Project Member, Software Dev. Leader",
        tldr: "Development of a Maritime Object Detection and Tracking Algorithm Using Multi-Camera Views, Creation of a Training Dataset for Deep Learning Models, and Integration into Autonomous Ship Systems",
        icon: "ship",
        gradient: "from-blue-500 to-indigo-600",
        tags: ["Maritime Detection", "Multi-Camera", "MOTIE"],
        featured: true
    },
    {
        id: 4,
        title: "Ceiling Layout Estimation for Indoor Environment",
        shortTitle: "Ceiling Layout Estimation",
        period: "Mar. 2022 -- Dec. 2022",
        organization: "LG, South Korea",
        role: "Project Member, AI & Software Dev. Leader",
        tldr: "Development of a Ceiling Segmentation Model and Construction of a Ceiling Segmentation Dataset for Robust Floor Plan Generation Under Occlusion",
        icon: "building",
        gradient: "from-purple-500 to-pink-600",
        tags: ["Segmentation", "Floor Plan", "LG"],
        featured: false
    },
    {
        id: 5,
        title: "Development of Swarm USV Autonomous Navigation Algorithm",
        shortTitle: "Swarm USV Project",
        period: "Apr. 2020 -- Nov. 2024",
        organization: "Agency for Defense Development (ADD), South Korea",
        role: "Project Leader, AI & Software Dev. Leader",
        tldr: "Development of Technologies to Enhance Swarm Situation Awareness, and Integration into Multiple USVs: Intention Prediction and Maritime Object Detection",
        icon: "anchor",
        gradient: "from-green-500 to-emerald-600",
        tags: ["Swarm", "USV", "ADD"],
        featured: false,
        video: "https://www.youtube.com/watch?v=AyBg_Y-ayZ4",
        videoLabel: "[News]"
    },
    {
        id: 6,
        title: "Robotic IKEA Furniture Assembly from Assembly Manuals",
        shortTitle: "IKEA Assembly Project",
        period: "Apr. 2019 -- Mar. 2020",
        organization: "Ministry of Science and ICT (MSIT), South Korea",
        role: "Project Member, AI & Software Developer",
        tldr: "A Competition of AI-robot Systems for Assembly of IKEA Furniture from Assembly Manuals: Assembly-Part Instance Segmentation and Workflow Visualization",
        icon: "wrench",
        gradient: "from-orange-500 to-red-600",
        tags: ["Assembly", "Segmentation", "MSIT"],
        featured: false,
        video: "https://www.youtube.com/watch?v=faphlYbk_Jg",
        videoLabel: "[Video]"
    },
    {
        id: 7,
        title: "Deep Learning-Based Sound Event Detection in Game Environments for Haptic Feedback Generation",
        shortTitle: "Sound Event Detection",
        period: "Mar. 2019 -- Aug. 2019",
        organization: "Dongwoon Anatech, South Korea",
        role: "Project Member, AI & Software Developer",
        tldr: "Construction of a Sound Event Detection Dataset and Development of a Sound Event Detection Model in Game Environments",
        icon: "volume-2",
        gradient: "from-yellow-500 to-amber-600",
        tags: ["Sound Detection", "Haptic", "Dongwoon"],
        featured: false
    },
    {
        id: 8,
        title: "Artificial Intelligence-Based Algorithm Development for Sleep Analysis and Diagnosis of Sleep Apnea Syndromes",
        shortTitle: "Sleep Analysis Project",
        period: "Mar. 2018 -- Dec. 2019",
        organization: "Gwangju Institute of Science and Technology (GIST), South Korea",
        role: "Project Member, AI Developer",
        tldr: "Construction of a Polysomnography Database, Development of a Sleep Stage Classification Model, and Development of a Sleep Apnea Detection Model",
        icon: "bed",
        gradient: "from-indigo-500 to-purple-600",
        tags: ["Sleep Analysis", "Medical AI", "GIST"],
        featured: false
    }
];

// Function to get featured projects (first 3)
function getFeaturedProjects() {
    return projectsData.filter(project => project.featured).slice(0, 3);
}

// Function to get all projects
function getAllProjects() {
    return projectsData;
} 