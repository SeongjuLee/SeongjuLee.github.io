// Awards Data
const awardsData = [
    {
        date: "Dec. 2024",
        title: "USV-based Obstacle Segmentation Challenge, 3rd Maritime Computer Vision Workshop",
        venue: "The 37th IEEE/CVF Winter Conference on Applications of Computer Vision (WACV 2025)",
        award: "First Prize",
        icon: "gold",
        description: "Maritime computer vision challenge for obstacle segmentation on unmanned surface vehicles"
    },
    {
        date: "Dec. 2024",
        title: "USV-based Panoptic Segmentation Challenge, 3rd Maritime Computer Vision Workshop",
        venue: "The 37th IEEE/CVF Winter Conference on Applications of Computer Vision (WACV 2025)",
        award: "Second Prize",
        icon: "silver",
        description: "Maritime computer vision challenge for panoptic segmentation on unmanned surface vehicles"
    },
    {
        date: "Sep. 2022",
        title: "The first NIA-GIST AI-HUB AI Competition",
        venue: "NIA, GIST",
        award: "First Prize",
        icon: "gold",
        description: "AI competition organized by National Information Society Agency and GIST"
    },
    {
        date: "Mar. 2020",
        title: "Presidential Scholarship Awarded (GFP)",
        venue: "GIST",
        award: "Scholarship",
        icon: "scholarship",
        description: "Presidential scholarship"
    },
    {
        date: "Nov. 2017",
        title: "Track1, The first GIST Innovative Convergence Technology Contest",
        venue: "GIST",
        award: "President's Award",
        icon: "president",
        description: "First track of GIST's innovative convergence technology competition"
    },
    {
        date: "Nov. 2017",
        title: "Track2, The first GIST Innovative Convergence Technology Contest",
        venue: "GIST",
        award: "Dean of Mechanical Engineering's Award",
        icon: "dean",
        description: "Second track of GIST's innovative convergence technology competition"
    }
];

// Get all awards
function getAllAwards() {
    return awardsData;
}

// Get selected awards (for main page)
function getSelectedAwards() {
    return awardsData.slice(0, 3); // Show first 3 awards on main page
}

// Filter awards by year
function filterAwardsByYear(year) {
    if (year === 'all') {
        return awardsData;
    }
    return awardsData.filter(award => award.date.includes(year));
}

// Get unique years for filtering
function getUniqueYears() {
    const years = new Set();
    awardsData.forEach(award => {
        const year = award.date.split(' ')[1]; // Extract year from "Dec. 2024" format
        years.add(year);
    });
    return Array.from(years).sort((a, b) => b - a);
}

// Get unique award types for filtering
function getUniqueAwardTypes() {
    const types = new Set();
    awardsData.forEach(award => {
        if (award.award.includes('Prize')) types.add('Prize');
        if (award.award.includes('Award')) types.add('Award');
        if (award.award.includes('Scholarship')) types.add('Scholarship');
    });
    return Array.from(types);
} 