// Education data that can be shared between pages
const educationData = [
    {
        id: 1,
        period: "Mar. 2020 - Present",
        degree: "Ph.D. Course in School of Integrated Technology",
        institution: "Gwangju Institute of Science and Technology (GIST)",
        program: "Intelligent Robotics Program",
        advisor: "Prof. Kyoobin Lee",
        status: "present"
    },
    {
        id: 2,
        period: "Mar. 2018 - Feb. 2020",
        degree: "M.S. in School of Integrated Technology",
        institution: "Gwangju Institute of Science and Technology (GIST)",
        program: "Intelligent Robotics Program",
        advisor: "Prof. Kyoobin Lee",
        status: "past"
    },
    {
        id: 3,
        period: "Mar. 2014 - Feb. 2018",
        degree: "B.S. in Department of Mechanical Engineering",
        institution: "Gwangju Institute of Science and Technology (GIST)",
        advisor: "Prof. Kwanheng Lee",
        status: "past"
    },
    {
        id: 4,
        period: "Mar. 2012 - Feb. 2014",
        degree: "Early Graduation",
        institution: "Gangwon Science High School",
        status: "past"
    }
];

// Function to get all education entries
function getAllEducation() {
    return educationData;
}

// Function to get education by status
function getEducationByStatus(status) {
    return educationData.filter(education => education.status === status);
} 