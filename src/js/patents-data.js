// Patents Data
const patentsData = [
    {
        year: 2024,
        status: "Applied (KR)",
        title: "그래프 트랜스포머 기반 다중 관계 분석 네트워크를 통한 다중 객체의 경로 예측 방법 및 장치",
        patentNumber: "2024-0159740",
        inventors: ["이성주", "이준석", "유연국", "김태리", "이규빈"],
        description: "그래프 트랜스포머를 활용한 다중 객체 경로 예측 기술"
    },
    {
        year: 2024,
        status: "Registered (KR), Applied (PCT)",
        title: "부품조립계획장치",
        patentNumber: "10-2647402, PCT/KR2022/000032",
        inventors: ["이성주", "백승혁", "강래영", "박성호", "신성호", "육태경", "이주순", "이규빈"],
        description: "자동화된 부품 조립 계획 생성 시스템"
    },
    {
        year: 2022,
        status: "Registered (KR), Applied (PCT)",
        title: "실환경 물체 인식 방법 및 장치",
        patentNumber: "10-2662978, PCT/KR2022/008146",
        inventors: ["이성주", "신성호", "강래영", "박성호", "이규빈"],
        description: "실시간 환경에서의 물체 인식 및 처리 기술"
    },
    {
        year: 2021,
        status: "Registered (KR)",
        title: "비접촉 센서를 이용한 신체 상태 정보 획득 방법",
        patentNumber: "10-2249237",
        inventors: ["이성주", "서호건", "박덕환", "김문상", "이규빈"],
        description: "비접촉 방식의 생체 신호 측정 및 분석 기술"
    },
    {
        year: 2019,
        status: "Applied (PCT, KR)",
        title: "부품조립도 이해와 조립계획 생성 시스템",
        patentNumber: "PCT/KR2022/000032, 2019-0153768",
        inventors: ["이성주", "백승혁", "강래영", "박성호", "신성호", "육태경", "이주순", "이규빈"],
        description: "조립도 분석 및 자동 조립 계획 생성 시스템"
    }
];

// Get all patents
function getAllPatents() {
    return patentsData;
}

// Get selected patents (for main page)
function getSelectedPatents() {
    return patentsData.slice(0, 3); // Show first 3 patents on main page
}

// Filter patents by status
function filterPatentsByStatus(status) {
    if (status === 'all') {
        return patentsData;
    }
    return patentsData.filter(patent => patent.status.includes(status));
}

// Filter patents by year
function filterPatentsByYear(year) {
    if (year === 'all') {
        return patentsData;
    }
    return patentsData.filter(patent => patent.year === parseInt(year));
}

// Get unique years for filtering
function getUniqueYears() {
    return [...new Set(patentsData.map(patent => patent.year))].sort((a, b) => b - a);
}

// Get unique statuses for filtering
function getUniqueStatuses() {
    const statuses = new Set();
    patentsData.forEach(patent => {
        if (patent.status.includes('Registered')) statuses.add('Registered');
        if (patent.status.includes('Applied')) statuses.add('Applied');
        if (patent.status.includes('PCT')) statuses.add('PCT');
    });
    return Array.from(statuses);
} 