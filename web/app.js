/**
 * ScoutEdge Glassmorphic Web Dashboard Application Logic
 */

const ATHLETE_DATASETS = {
    julian_vance: {
        name: "Julian Vance",
        position: "Attacking Midfield",
        team: "Apex Youth Academy",
        league: "U21 National Division",
        fitScore: 87.3,
        recommendation: "SIGN / HIGH PRIORITY TARGET",
        se_r: 92.6,
        percentile: 90.4,
        technical: 88,
        tactical: 85,
        physical: 82,
        se_r_driver: "✓ High technical proficiency observed by scouts",
        pgi: 76.0,
        stage: "Emerging Potential",
        ceiling: 91.2,
        velocity: "+2.4 / match",
        pgi_driver: "✓ Accelerated trajectory over recent match logs",
        readiness: 95.2,
        acwr: "1.00",
        risk: "Low Risk",
        mins: "90 Mins",
        edge_driver: "✓ Optimal acute-to-chronic workload balance",
        fin_category: "UNDERVALUED OPPORTUNITY",
        fin_vfm: "100.0 / 100",
        fin_roi: "+15.0% 3-Yr Resale ROI",
        market_val: "€12.5M",
        wage: "€35,000",
        contract: "1.0 Years",
        reasons: [
            "✓ High performance-to-cost ratio (7.59 SE-R pts / €1M)",
            "✓ Low workload injury risk profile (EdgeCare™)",
        ],
    },
    kylian_mbappe: {
        name: "Kylian Mbappe-Vance",
        position: "Left Winger",
        team: "Capital City Elite",
        league: "Division 1 Professional",
        fitScore: 90.5,
        recommendation: "SIGN / HIGH PRIORITY TARGET",
        se_r: 97.1,
        percentile: 94.7,
        technical: 94,
        tactical: 88,
        physical: 96,
        se_r_driver: "✓ Exceptional statistical performance & sprint velocity",
        pgi: 78.2,
        stage: "Emerging Potential",
        ceiling: 99.0,
        velocity: "+3.1 / match",
        pgi_driver: "✓ Elite growth ceiling trajectory",
        readiness: 97.2,
        acwr: "1.00",
        risk: "Low Risk",
        mins: "90 Mins",
        edge_driver: "✓ Consistent workload availability",
        fin_category: "PREMIUM / HIGH VALUE",
        fin_vfm: "88.5 / 100",
        fin_roi: "+22.0% 3-Yr Resale ROI",
        market_val: "€45.0M",
        wage: "€120,000",
        contract: "2.5 Years",
        reasons: [
            "✓ World-class rating baseline (SE-R™: 97.1)",
            "✓ High 3-year resale ROI projection (+22.0%)",
        ],
    },
    arda_guler: {
        name: "Arda Guler-Vance",
        position: "Playmaker",
        team: "Iberia Sports Club",
        league: "Division 1",
        fitScore: 89.5,
        recommendation: "SIGN / HIGH PRIORITY TARGET",
        se_r: 94.9,
        percentile: 92.8,
        technical: 92,
        tactical: 88,
        physical: 82,
        se_r_driver: "✓ High technical proficiency & key pass volume",
        pgi: 80.5,
        stage: "Early Development",
        ceiling: 95.0,
        velocity: "+3.5 / match",
        pgi_driver: "✓ High upside age-curve dynamic",
        readiness: 96.0,
        acwr: "1.00",
        risk: "Low Risk",
        mins: "90 Mins",
        edge_driver: "✓ Excellent fatigue recovery score",
        fin_category: "UNDERVALUED OPPORTUNITY",
        fin_vfm: "100.0 / 100",
        fin_roi: "+25.0% 3-Yr Resale ROI",
        market_val: "€12.5M",
        wage: "€35,000",
        contract: "1.0 Years",
        reasons: [
            "✓ Contract expiring soon (< 1 year remaining) - Leverage opportunity",
            "✓ High performance-to-cost ratio (7.59 SE-R pts / €1M)",
        ],
    },
    florian_wirtz: {
        name: "Florian Wirtz",
        position: "Advanced Midfield",
        team: "Rhine Valley FC",
        league: "Bundesliga",
        fitScore: 86.7,
        recommendation: "SHORTLIST & MONITOR DEVELOPMENT",
        se_r: 91.1,
        percentile: 89.0,
        technical: 92,
        tactical: 90,
        physical: 85,
        se_r_driver: "✓ Exceptional spatial awareness & chance creation",
        pgi: 75.3,
        stage: "Emerging Potential",
        ceiling: 99.0,
        velocity: "+1.8 / match",
        pgi_driver: "✓ Steady developmental baseline",
        readiness: 96.8,
        acwr: "1.00",
        risk: "Low Risk",
        mins: "90 Mins",
        edge_driver: "✓ Low workload injury risk profile",
        fin_category: "FAIR MARKET VALUE",
        fin_vfm: "65.0 / 100",
        fin_roi: "+12.0% 3-Yr Resale ROI",
        market_val: "€35.0M",
        wage: "€85,000",
        contract: "3.0 Years",
        reasons: [
            "✓ High technical rating baseline (92.0)",
            "✓ Market value accurately aligns with SE-R™ rating output",
        ],
    },
};

document.addEventListener("DOMContentLoaded", () => {
    const athleteSelect = document.getElementById("athleteSelect");
    const sliderPassAcc = document.getElementById("sliderPassAcc");
    const sliderScoutTech = document.getElementById("sliderScoutTech");
    const sliderWorkload = document.getElementById("sliderWorkload");
    const btnRecalculate = document.getElementById("btnRecalculate");

    function renderAthlete(key) {
        const data = ATHLETE_DATASETS[key] || ATHLETE_DATASETS.julian_vance;
        
        document.getElementById("recBadge").textContent = data.recommendation;
        document.getElementById("fitScore").textContent = data.fitScore.toFixed(1);
        document.getElementById("athleteBio").textContent = `${data.name} • ${data.position} • ${data.team} (${data.league})`;
        
        document.getElementById("serRating").childNodes[0].nodeValue = data.se_r.toFixed(1) + " ";
        document.getElementById("serPercentile").textContent = data.percentile + "%";
        document.getElementById("serTech").textContent = data.technical.toFixed(1);
        document.getElementById("serTact").textContent = data.tactical.toFixed(1);
        document.getElementById("serPhys").textContent = data.physical.toFixed(1);
        
        document.getElementById("fillTech").style.width = data.technical + "%";
        document.getElementById("fillTact").style.width = data.tactical + "%";
        document.getElementById("fillPhys").style.width = data.physical + "%";
        document.getElementById("serDriver").textContent = data.se_r_driver;

        document.getElementById("pgiScore").childNodes[0].nodeValue = data.pgi.toFixed(1) + " ";
        document.getElementById("pgiStage").textContent = data.stage;
        document.getElementById("pgiCeiling").textContent = data.ceiling.toFixed(1);
        document.getElementById("pgiVelocity").textContent = data.velocity;
        document.getElementById("pgiDriver").textContent = data.pgi_driver;

        document.getElementById("edgeReadiness").childNodes[0].nodeValue = data.readiness.toFixed(1) + " ";
        document.getElementById("edgeACWR").textContent = data.acwr;
        document.getElementById("edgeRisk").textContent = data.risk;
        document.getElementById("edgeMins").textContent = data.mins;
        document.getElementById("edgeDriver").textContent = data.edge_driver;

        document.getElementById("finCategory").textContent = data.fin_category;
        document.getElementById("finVfm").textContent = data.fin_vfm;
        document.getElementById("finRoi").textContent = data.fin_roi;
        document.getElementById("finMarketVal").textContent = data.market_val;
        document.getElementById("finWage").textContent = data.wage;
        document.getElementById("finContract").textContent = data.contract;

        const reasonsContainer = document.getElementById("explainReasons");
        reasonsContainer.innerHTML = "";
        data.reasons.forEach(reason => {
            const div = document.createElement("div");
            div.className = "reason-chip";
            div.textContent = reason;
            reasonsContainer.appendChild(div);
        });

        sliderScoutTech.value = data.technical;
        document.getElementById("lblScoutTech").textContent = data.technical;
    }

    // Dropdown change listener
    athleteSelect.addEventListener("change", (e) => {
        renderAthlete(e.target.value);
    });

    // Slider Listeners
    sliderPassAcc.addEventListener("input", (e) => {
        document.getElementById("lblPassAcc").textContent = e.target.value + "%";
    });
    sliderScoutTech.addEventListener("input", (e) => {
        document.getElementById("lblScoutTech").textContent = e.target.value;
    });
    sliderWorkload.addEventListener("input", (e) => {
        document.getElementById("lblWorkload").textContent = e.target.value + " Mins";
    });

    // Recalculate Listener
    btnRecalculate.addEventListener("click", () => {
        const passAcc = parseFloat(sliderPassAcc.value);
        const scoutTech = parseFloat(sliderScoutTech.value);
        const workload = parseFloat(sliderWorkload.value);

        // Dynamic score adjustment formula
        const currentAthleteKey = athleteSelect.value;
        const base = ATHLETE_DATASETS[currentAthleteKey];

        const newSER = Math.min(Math.max((scoutTech * 0.6) + (passAcc * 0.4), 40), 99);
        const newReadiness = Math.min(Math.max(100 - (workload / 10), 50), 99);
        const newFit = (newSER * 0.5) + (base.pgi * 0.3) + (newReadiness * 0.2);

        document.getElementById("serRating").childNodes[0].nodeValue = newSER.toFixed(1) + " ";
        document.getElementById("serTech").textContent = scoutTech.toFixed(1);
        document.getElementById("fillTech").style.width = scoutTech + "%";
        document.getElementById("edgeReadiness").childNodes[0].nodeValue = newReadiness.toFixed(1) + " ";
        document.getElementById("fitScore").textContent = newFit.toFixed(1);

        if (newFit >= 85) {
            document.getElementById("recBadge").textContent = "SIGN / HIGH PRIORITY TARGET";
        } else if (newFit >= 70) {
            document.getElementById("recBadge").textContent = "SHORTLIST & MONITOR DEVELOPMENT";
        } else {
            document.getElementById("recBadge").textContent = "DEVELOP IN ACADEMY";
        }
    });

    // Initial render
    renderAthlete("julian_vance");
});
