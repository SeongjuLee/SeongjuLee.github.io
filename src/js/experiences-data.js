// Experiences Data
const experiencesData = [
    {
        period: "Mar. 2024 -- Present",
        role: "Lab Server Administrator",
        organization: "GIST",
        position: "Leader",
        description: "GPU Server Maintenance (Expansion and Management)",
        details: [
            "GPU Server Maintenance (Expansion and Management)",
            "Developed Multi-server Distributed Parallel Learning System using Slurm",
            "Developed a Real-time Multi-server GPU and Storage Monitoring Dashboard Website"
        ],
        type: "Administration"
    },
    {
        period: "Mar. 2022 -- Feb. 2025",
        role: "Technical Research Personnel",
        organization: "GIST",
        position: "",
        description: "",
        details: [],
        type: "Research"
    },
    {
        period: "Sep. 2021 -- Dec. 2021",
        role: "Teaching Assistant",
        organization: "GIST",
        position: "",
        description: "",
        details: ["Advanced Deep Learning (RT5102, Fall)"],
        type: "Teaching"
    },
    {
        period: "Mar. 2021 -- Jun. 2021",
        role: "Teaching Assistant",
        organization: "GIST",
        position: "",
        description: "",
        details: ["Deep Learning (RT5101, Spring)"],
        type: "Teaching"
    },
    {
        period: "Mar. 2020 -- Jun. 2020",
        role: "Teaching Assistant",
        organization: "GIST",
        position: "",
        description: "",
        details: ["Deep Learning (RT5101, Spring)"],
        type: "Teaching"
    },
    {
        period: "Mar. 2019 -- Jun. 2019",
        role: "Teaching Assistant",
        organization: "GIST",
        position: "",
        description: "",
        details: ["Deep Learning (RT5101, Spring)"],
        type: "Teaching"
    },
    {
        period: "Nov. 2017 -- Feb. 2018",
        role: "Intern at Artificial Intelligence Laboratory",
        organization: "GIST",
        position: "",
        description: "",
        details: ["Advisor: Prof. Kyoobin Lee"],
        type: "Internship"
    },
    {
        period: "Jul. 2017 -- Aug. 2017",
        role: "Intern at Healthcare Robotics Laboratory",
        organization: "GIST",
        position: "",
        description: "",
        details: ["Advisor: Prof. Munsang Kim"],
        type: "Internship"
    },
    {
        period: "Dec. 2015 -- Mar. 2016",
        role: "Intern at Intelligence Design and Graphics Laboratory",
        organization: "GIST",
        position: "",
        description: "",
        details: ["Advisor: Prof. Kwanheng Lee"],
        type: "Internship"
    },
    {
        period: "Jul. 2015 -- Aug. 2015",
        role: "Summer Session Extension",
        organization: "University of California, Berkeley",
        position: "",
        description: "",
        details: ["Linear Algebra and Differential Equations", "Social Inequalities"],
        type: "Education"
    }
];

// Get all experiences
function getAllExperiences() {
    return experiencesData;
}

// Get selected experiences (for main page)
function getSelectedExperiences() {
    return experiencesData.slice(0, 3); // Show first 3 experiences on main page
}

// Filter experiences by type
function filterExperiencesByType(type) {
    if (type === 'all') {
        return experiencesData;
    }
    return experiencesData.filter(experience => experience.type === type);
}

// Get unique types for filtering
function getUniqueTypes() {
    const types = new Set();
    experiencesData.forEach(experience => {
        types.add(experience.type);
    });
    return Array.from(types);
}

// Get experiences by organization
function getExperiencesByOrganization(organization) {
    return experiencesData.filter(experience => experience.organization === organization);
} 