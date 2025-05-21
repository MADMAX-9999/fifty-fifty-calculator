import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const StrategyCalculator = () => {
  // Strategie i ich zakresy
  const strategies = [
    { 
      name: "START", 
      minValue: 5000, 
      maxValue: 9999, 
      description: "Fundamentalny pierwszy krok w budowaniu trwałego, materialnego majątku zabezpieczonego przed inflacją",
      minPurchase: 100,
      maxPurchase: 1000,
      minYears: 7,
      maxYears: 30,
      yearsDescription: "Horyzont czasowy 7-30+ lat stanowi perspektywę dla budowy solidnych podstaw majątkowych",
      step: 250
    },
    { 
      name: "BALANCE", 
      minValue: 10000, 
      maxValue: 99999, 
      description: "Zaawansowana dywersyfikacja majątku poprzez zrównoważoną alokację kapitału między różne klasy metali",
      minPurchase: 250,
      maxPurchase: 2500,
      minYears: 7,
      maxYears: 30,
      yearsDescription: "Perspektywa 7-30+ lat to początek drogi ku stworzeniu trwałego majątku rodzinnego",
      step: 500
    },
    { 
      name: "FOUNDATION", 
      minValue: 100000, 
      maxValue: 699999,
      description: "Kompleksowe rozwiązanie dla budowania solidnego fundamentu majątkowego opartego na materialnych aktywach",
      minPurchase: 500,
      maxPurchase: 5000,
      minYears: 15,
      maxYears: 30,
      yearsDescription: "Horyzont 15-30+ lat to optymalny okres dla ukazania pełnego potencjału strategii",
      step: 5000
    },
    { 
      name: "OPTIMAL", 
      minValue: 700000, 
      maxValue: 2099999, 
      description: "Zaawansowane rozwiązanie dla tworzenia znaczącego majątku materialnego o najwyższym stopniu odporności",
      minPurchase: 1000,
      maxPurchase: 20000,
      minYears: 15,
      maxYears: 30,
      yearsDescription: "Perspektywa 15-30+ lat stanowi ramę czasową dla strategicznego rozwoju portfela",
      step: 10000
    },
    { 
      name: "PRESTIGE", 
      minValue: 2100000, 
      maxValue: 5000000, 
      description: "Kwintesencja budowania dynastycznego majątku materialnego z dominującym udziałem metali strategicznych",
      minPurchase: 2500,
      maxPurchase: 50000,
      minYears: 20,
      maxYears: 30,
      yearsDescription: "Perspektywa 20-30+ lat odzwierciedla horyzont planowania ponadpokoleniowego majątku",
      step: 25000
    }
  ];

  // Informacje o taryfach depozytowych
  const depositTariffs = {
    START: [
      { 
        name: "GTS",
        minValue: 5000,
        maxValue: 9999,
        agio: "3,5% kwoty aktywacji",
        metals: "40% złoto, 20% srebro, 20% platyna, 20% pallad",
        storage: "1,5% netto + VAT rocznie",
        advantages: ["Niski próg wejścia", "Prostota zarządzania", "Ekspozycja na podstawowe metale szlachetne", "Zakupy dodatkowe bez AGIO"],
        details: "Zakupy dodatkowe: 100-1.000 EUR/tydzień bez AGIO"
      }
    ],
    BALANCE: [
      { 
        name: "GTS + GR S-3",
        minValue: 10000,
        maxValue: 29999,
        agio: "3,5% dla SSW + 300 EUR (stała kwota) dla Auvesta",
        metals: "GTS: 40% złoto, 20% srebro, 20% platyna, 20% pallad | GR: 50% złoto, 50% srebro",
        storage: "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,08% netto + VAT miesięcznie",
        advantages: ["Równowaga między dostawcami", "Dywersyfikacja metali", "AGIO w GR zwracane w 100% jako bonus metali", "Zakupy dodatkowe bez AGIO"],
        details: "Podział 50/50 między SSW (GTS) i Auvesta (GR). Zakupy dodatkowe: 250-2.500 EUR/tydzień bez AGIO."
      },
      { 
        name: "GTS + GR M-6",
        minValue: 30000,
        maxValue: 49999,
        agio: "3,5% dla SSW + 600 EUR (stała kwota) dla Auvesta",
        metals: "GTS: 40% złoto, 20% srebro, 20% platyna, 20% pallad | GR: 50% złoto, 50% srebro",
        storage: "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,07% netto + VAT miesięcznie",
        advantages: ["Równowaga między dostawcami", "Dywersyfikacja metali", "AGIO w GR zwracane w 100% jako bonus metali", "Ceny zakupu metali: 1% taniej od taryfy S-3"],
        details: "Podział 50/50 między SSW (GTS) i Auvesta (GR). Zakupy dodatkowe: 250-2.500 EUR/tydzień bez AGIO."
      },
      { 
        name: "GTS + GR L-12",
        minValue: 50000,
        maxValue: 99999,
        agio: "3,5% dla SSW + 1.200 EUR (stała kwota) dla Auvesta",
        metals: "GTS: 40% złoto, 20% srebro, 20% platyna, 20% pallad | GR: 50% złoto, 50% srebro",
        storage: "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,06% netto + VAT miesięcznie",
        advantages: ["Równowaga między dostawcami", "Dywersyfikacja metali", "AGIO w GR zwracane w 100% jako bonus metali", "Ceny zakupu metali: 3% taniej od taryfy S-3"],
        details: "Podział 50/50 między SSW (GTS) i Auvesta (GR). Zakupy dodatkowe: 250-2.500 EUR/tydzień bez AGIO."
      }
    ],
    FOUNDATION: [
      { 
        name: "GT + GR XL-24",
        minValue: 100000,
        maxValue: 299999,
        agio: "3,5% dla SSW + 2.400 EUR (stała kwota) dla Auvesta",
        metals: "GT: 20% złoto, 10% srebro, 10% platyna, 10% pallad, 50% metale strategiczne | GR: 50% złoto, 50% srebro",
        storage: "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,05% netto + VAT miesięcznie",
        advantages: ["Dostęp do metali strategicznych", "Optymalne koszty magazynowania", "AGIO w GR zwracane w 100% jako bonus metali", "Ceny zakupu metali: 6% taniej od taryfy S-3"],
        details: "Podział 50/50 między SSW (GT) i Auvesta (GR). Zakupy dodatkowe: 500-5.000 EUR/tydzień bez AGIO."
      },
      { 
        name: "GT + GR VIP",
        minValue: 300000,
        maxValue: 699999,
        agio: "3,5% dla SSW + 2.400 EUR (stała kwota) dla Auvesta",
        metals: "GT: 20% złoto, 10% srebro, 10% platyna, 10% pallad, 50% metale strategiczne | GR: 50% złoto, 50% srebro",
        storage: "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,04% netto + VAT miesięcznie",
        advantages: ["Dostęp do metali strategicznych", "Optymalne koszty magazynowania", "AGIO w GR zwracane w 100% jako bonus metali", "Ceny zakupu metali: 7% taniej od taryfy S-3"],
        details: "Podział 50/50 między SSW (GT) i Auvesta (GR). Zakupy dodatkowe: 500-5.000 EUR/tydzień bez AGIO."
      }
    ],
    OPTIMAL: [
      { 
        name: "GT + GR VIP",
        minValue: 700000,
        maxValue: 2099999,
        agio: "3,5% dla SSW + 2.400 EUR za każde 150.000 EUR dla Auvesta",
        metals: "GT: 20% złoto, 10% srebro, 10% platyna, 10% pallad, 50% metale strategiczne | GR: 50% złoto, 50% srebro",
        storage: "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,04% netto + VAT miesięcznie",
        advantages: ["Maksymalna efektywność kosztowa", "Idealna dywersyfikacja", "Dostęp do taryf VIP", "Ceny zakupu metali: 7% taniej od taryfy S-3"],
        details: "Podział 50/50 między SSW (GT) i Auvesta (GR). Dla kwot powyżej 900.000 EUR zalecany podział na maksymalnie 6 depozytów VIP. Zakupy dodatkowe: 1.000-20.000 EUR/tydzień bez AGIO."
      }
    ],
    PRESTIGE: [
      { 
        name: "GTS + GT + GR VIP + SMH",
        minValue: 2100000,
        maxValue: 5000000,
        agio: "3,5% dla SSW (GTS, GT) + 2.400 EUR za każde 150.000 EUR dla Auvesta + 0% dla SMH",
        metals: "Złożony portfel w proporcjach: 10% GTS, 20% GT, 30% GR, 40% SMH",
        storage: "SSW: 1,5% netto + VAT rocznie | Auvesta: 0,04% netto + VAT miesięcznie",
        advantages: ["Maksymalna dywersyfikacja", "Dominujący udział metali strategicznych (SMH)", "Najniższe koszty utrzymania", "Dedykowany komponent dla metali strategicznych"],
        details: "Podział: 10% GTS, 20% GT, 30% GR, 40% SMH. Zakupy dodatkowe: 2.500-50.000 EUR/tydzień bez AGIO."
      }
    ]
  };

  // Stan aplikacji - rozpocznij od FOUNDATION i 20 lat
  const [strategy, setStrategy] = useState(2);
  const [amount, setAmount] = useState(strategies[2].minValue);
  const [purchase, setPurchase] = useState(strategies[2].minPurchase);
  const [viewMode, setViewMode] = useState("metals");
  const [yearsValue, setYearsValue] = useState(20);
  const [showDeposits, setShowDeposits] = useState(false);
  const [activeTabIndex, setActiveTabIndex] = useState(0);

  // Aktualizacja kwot przy zmianie strategii
  useEffect(() => {
    const current = strategies[strategy];
    setAmount(Math.ceil((current.minValue + current.maxValue) / 2));
    setPurchase(Math.ceil((current.minPurchase + current.maxPurchase) / 2));
    if (yearsValue < current.minYears) {
      setYearsValue(current.minYears);
    }
  }, [strategy]);

  // Formatowanie kwot
  const formatEUR = (value) => {
    return new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(value);
  };

  // Wyświetlanie lat
  const getYearsDisplay = () => {
    return yearsValue >= 30 ? "30+" : yearsValue;
  };

  // Alokacja metali
  const getMetals = () => {
    const current = strategies[strategy];
    if (current.name === "START") {
      return [
        { name: 'Złoto', value: 40, amount: amount * 0.4, color: '#FFD700' },
        { name: 'Srebro', value: 20, amount: amount * 0.2, color: '#C0C0C0' },
        { name: 'Platyna', value: 20, amount: amount * 0.2, color: '#E5E4E2' },
        { name: 'Pallad', value: 20, amount: amount * 0.2, color: '#B9F2FF' }
      ];
    } else if (current.name === "BALANCE") {
      return [
        { name: 'Złoto', value: 45, amount: amount * 0.45, color: '#FFD700' },
        { name: 'Srebro', value: 35, amount: amount * 0.35, color: '#C0C0C0' },
        { name: 'Platyna', value: 10, amount: amount * 0.1, color: '#E5E4E2' },
        { name: 'Pallad', value: 10, amount: amount * 0.1, color: '#B9F2FF' }
      ];
    } else if (current.name === "FOUNDATION" || current.name === "OPTIMAL") {
      return [
        { name: 'Złoto', value: 35, amount: amount * 0.35, color: '#FFD700' },
        { name: 'Srebro', value: 30, amount: amount * 0.3, color: '#C0C0C0' },
        { name: 'Platyna', value: 5, amount: amount * 0.05, color: '#E5E4E2' },
        { name: 'Pallad', value: 5, amount: amount * 0.05, color: '#B9F2FF' },
        { name: 'Hafn', value: 5, amount: amount * 0.05, color: '#A9A9A9' },
        { name: 'Gal', value: 5, amount: amount * 0.05, color: '#6495ED' },
        { name: 'Ind', value: 5, amount: amount * 0.05, color: '#9370DB' },
        { name: 'German', value: 5, amount: amount * 0.05, color: '#808080' },
        { name: 'Tantal', value: 5, amount: amount * 0.05, color: '#708090' }
      ];
    } else {
      // Tylko w PRESTIGE mamy 40% metali strategicznych
      return [
        { name: 'Złoto', value: 25, amount: amount * 0.25, color: '#FFD700' },
        { name: 'Srebro', value: 20, amount: amount * 0.2, color: '#C0C0C0' },
        { name: 'Platyna', value: 5, amount: amount * 0.05, color: '#E5E4E2' },
        { name: 'Pallad', value: 5, amount: amount * 0.05, color: '#B9F2FF' },
        { name: 'Metale Strategiczne', value: 40, amount: amount * 0.4, color: '#4169E1' },
        { name: 'Hafn', value: 1, amount: amount * 0.01, color: '#A9A9A9' },
        { name: 'Gal', value: 1, amount: amount * 0.01, color: '#6495ED' },
        { name: 'Ind', value: 1, amount: amount * 0.01, color: '#9370DB' },
        { name: 'German', value: 1, amount: amount * 0.01, color: '#808080' },
        { name: 'Tantal', value: 1, amount: amount * 0.01, color: '#708090' }
      ];
    }
  };

  // Struktura komponentów
  const getComponents = () => {
    const current = strategies[strategy];
    if (current.name === "START") {
      return [
        { name: 'GTS (SSW)', value: 100, amount: amount, color: '#FFD700' }
      ];
    } else if (current.name === "BALANCE" || current.name === "FOUNDATION" || current.name === "OPTIMAL") {
      return [
        { name: current.name === "BALANCE" ? 'GTS (SSW)' : 'GT (SSW)', value: 50, amount: amount * 0.5, color: '#FFD700' },
        { name: 'GR (Auvesta)', value: 50, amount: amount * 0.5, color: '#C0C0C0' }
      ];
    } else {
      return [
        { name: 'GTS (SSW)', value: 10, amount: amount * 0.1, color: '#FFD700' },
        { name: 'GT (SSW)', value: 20, amount: amount * 0.2, color: '#E5E4E2' },
        { name: 'GR (Auvesta)', value: 30, amount: amount * 0.3, color: '#C0C0C0' },
        { name: 'SMH (SSW)', value: 40, amount: amount * 0.4, color: '#6495ED' }
      ];
    }
  };

  // Obliczenie AGIO
  const getAgio = () => {
    const current = strategies[strategy];
    let initialAgio = 0;
    let bonus = 0;
    
    if (current.name === "START") {
      initialAgio = amount * 0.035; // 3.5%
    } else if (current.name === "BALANCE" || current.name === "FOUNDATION" || current.name === "OPTIMAL") {
      const sswAgio = amount * 0.5 * 0.035; // 3.5% dla SSW
      let auvestaAgio = 0;
      
      const auvestaAmount = amount * 0.5;
      if (auvestaAmount < 15000) {
        auvestaAgio = 300; // S-3
      } else if (auvestaAmount < 25000) {
        auvestaAgio = 600; // M-6
      } else if (auvestaAmount < 50000) {
        auvestaAgio = 1200; // L-12
      } else if (auvestaAmount < 150000) {
        auvestaAgio = 2400; // XL-24
      } else {
        const vipCount = Math.min(6, Math.ceil(auvestaAmount / 150000));
        auvestaAgio = vipCount * 2400; // VIP
      }
      
      initialAgio = sswAgio + auvestaAgio;
      bonus = auvestaAgio; // 100% zwrotu
    } else {
      const gtsAgio = amount * 0.1 * 0.035;
      const gtAgio = amount * 0.2 * 0.035;
      const grAmount = amount * 0.3;
      const grCount = Math.min(6, Math.ceil(grAmount / 150000));
      const grAgio = grCount * 2400;
      
      initialAgio = gtsAgio + gtAgio + grAgio;
      bonus = grAgio;
    }
    
    const effectiveAgio = initialAgio - bonus;
    const initialPercent = (initialAgio / amount) * 100;
    const effectivePercent = (effectiveAgio / amount) * 100;
    
    return { initialAgio, bonus, effectiveAgio, initialPercent, effectivePercent };
  };

  // Znajdowanie odpowiedniej taryfy dla bieżącej kwoty
  const getCurrentTariff = () => {
    const current = strategies[strategy];
    const tariffs = depositTariffs[current.name];
    return tariffs.find(t => t.minValue <= amount && amount <= t.maxValue);
  };

  // Dane dla wykresów
  const metals = getMetals();
  const components = getComponents();
  const agio = getAgio();
  const currentTariff = getCurrentTariff();

  const handleTabClick = (index) => {
    setActiveTabIndex(index);
    if (index === 0) {
      setViewMode("metals");
      setShowDeposits(false);
    } else if (index === 1) {
      setViewMode("components"); 
      setShowDeposits(false);
    } else {
      setShowDeposits(true);
      setViewMode("none");
    }
  };

  return (
    <div className="flex flex-col gap-6 p-4 font-sans bg-gray-100 min-h-screen">
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <h1 className="text-3xl font-bold text-center text-blue-800 mb-2">Kalkulator Strategii Fifty/Fifty</h1>
        <p className="text-center text-gray-600 mb-6">Optymalizacja alokacji aktywów w metale szlachetne i strategiczne</p>
        
        <div className="bg-blue-50 p-4 rounded-lg shadow mb-6">
          <h2 className="text-xl font-semibold mb-4 text-blue-800">Konfiguracja Strategii</h2>
          
          <div className="flex flex-col space-y-6">
            <div className="space-y-2">
              <label className="font-medium flex justify-between">
                <span>Wybierz strategię:</span>
                <span className="text-blue-700 font-bold">{strategies[strategy].name}</span>
              </label>
              <input
                type="range"
                min="0"
                max="4"
                step="1"
                value={strategy}
                onChange={(e) => setStrategy(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-sm text-gray-600">
                {strategies.map((s, index) => (
                  <span key={index} className={strategy === index ? "font-bold text-blue-700" : ""}>
                    {s.name}
                  </span>
                ))}
              </div>
              <p className="mt-2 text-gray-700 italic bg-blue-100 p-3 rounded">{strategies[strategy].description}</p>
            </div>
            
            <div className="space-y-2">
              <label className="font-medium flex justify-between">
                <span>Kwota alokacji:</span>
                <span className="text-blue-700 font-bold">{formatEUR(amount)}</span>
              </label>
              <input
                type="range"
                min={strategies[strategy].minValue}
                max={strategies[strategy].maxValue}
                step={strategies[strategy].step}
                value={amount}
                onChange={(e) => setAmount(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-sm text-gray-600">
                <span>{formatEUR(strategies[strategy].minValue)}</span>
                <span>{formatEUR(strategies[strategy].maxValue)}</span>
              </div>
            </div>
            
            <div className="space-y-2">
              <label className="font-medium flex justify-between">
                <span>Efekt Kursu Średniego:</span>
                <span className="text-blue-700 font-bold">{formatEUR(purchase)} / tydzień</span>
              </label>
              <input
                type="range"
                min={strategies[strategy].minPurchase}
                max={strategies[strategy].maxPurchase}
                step={strategy === 0 ? 50 : 
                     strategy === 1 ? 50 : 
                     strategy === 2 ? 250 : 
                     strategy === 3 ? 500 : 500}
                value={purchase}
                onChange={(e) => setPurchase(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-sm text-gray-600">
                <span>{formatEUR(strategies[strategy].minPurchase)}</span>
                <span>{formatEUR(strategies[strategy].maxPurchase)}</span>
              </div>
              <div className="mt-1 text-sm text-gray-600 italic">
                Regularne dokupienia metali dla optymalizacji średniej ceny zakupu
              </div>
            </div>
            
            <div className="space-y-2">
              <label className="font-medium flex justify-between">
                <span>Perspektywa budowy fundamentu:</span>
                <span className="text-blue-700 font-bold">{getYearsDisplay()} lat</span>
              </label>
              <input
                type="range"
                min={strategies[strategy].minYears}
                max={strategies[strategy].maxYears}
                step="1"
                value={Math.min(yearsValue, strategies[strategy].maxYears)}
                onChange={(e) => setYearsValue(parseInt(e.target.value))}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <div className="flex justify-between text-sm text-gray-600">
                <span>{strategies[strategy].minYears} lat</span>
                <span>30+ lat</span>
              </div>
              <div className="mt-1 text-sm text-gray-600 italic">
                {strategies[strategy].yearsDescription}
              </div>
            </div>
          </div>
        </div>
        
        {/* Zakładki */}
        <div className="mb-6">
          <div className="flex border-b border-gray-200">
            <button 
              onClick={() => handleTabClick(0)}
              className={`px-4 py-2 font-medium rounded-t-lg ${activeTabIndex === 0 
                ? "bg-blue-600 text-white border-b-2 border-blue-600" 
                : "bg-gray-100 hover:bg-gray-200"}`}
            >
              Alokacja metali
            </button>
            <button 
              onClick={() => handleTabClick(1)}
              className={`px-4 py-2 font-medium rounded-t-lg ${activeTabIndex === 1 
                ? "bg-blue-600 text-white border-b-2 border-blue-600" 
                : "bg-gray-100 hover:bg-gray-200"}`}
            >
              Struktura komponentów
            </button>
            <button 
              onClick={() => handleTabClick(2)}
              className={`px-4 py-2 font-medium rounded-t-lg ${activeTabIndex === 2 
                ? "bg-blue-600 text-white border-b-2 border-blue-600" 
                : "bg-gray-100 hover:bg-gray-200"}`}
            >
              Taryfy depozytowe
            </button>
          </div>
        </div>

        {showDeposits ? (
          <div className="bg-white p-4 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4 text-blue-800">Taryfy depozytowe dla strategii {strategies[strategy].name}</h2>
            
            {depositTariffs[strategies[strategy].name].map((tariff, index) => (
              <div key={index} className={`mb-6 p-4 rounded-lg shadow ${tariff.minValue <= amount && amount <= tariff.maxValue ? "bg-blue-50 border-l-4 border-blue-500" : "bg-white"}`}>
                <div className="flex flex-col md:flex-row justify-between">
                  <div>
                    <h3 className="text-lg font-bold text-blue-700">{tariff.name}</h3>
                    <p className="text-gray-600">Kwota: {formatEUR(tariff.minValue)} - {formatEUR(tariff.maxValue)}</p>
                  </div>
                  <div className="mt-2 md:mt-0">
                    <span className={`px-3 py-1 rounded-full text-sm ${tariff.minValue <= amount && amount <= tariff.maxValue 
                      ? "bg-green-100 text-green-800 font-medium" 
                      : "bg-gray-100 text-gray-600"}`}>
                      {tariff.minValue <= amount && amount <= tariff.maxValue ? "✓ Dostępna dla aktualnej kwoty" : "Poza aktualnym zakresem"}
                    </span>
                  </div>
                </div>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                  <div className="bg-gray-50 p-3 rounded">
                    <h4 className="font-semibold text-gray-700">AGIO:</h4>
                    <p className="text-gray-600">{tariff.agio}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded">
                    <h4 className="font-semibold text-gray-700">Koszty magazynowania:</h4>
                    <p className="text-gray-600">{tariff.storage}</p>
                  </div>
                </div>
                
                <div className="mt-4 bg-gray-50 p-3 rounded">
                  <h4 className="font-semibold text-gray-700">Alokacja metali:</h4>
                  <p className="text-gray-600">{tariff.metals}</p>
                </div>
                
                <div className="mt-4">
                  <h4 className="font-semibold text-gray-700">Zalety:</h4>
                  <ul className="list-disc pl-5 mt-2 text-gray-600 grid grid-cols-1 md:grid-cols-2 gap-2">
                    {tariff.advantages.map((advantage, idx) => (
                      <li key={idx}>{advantage}</li>
                    ))}
                  </ul>
                </div>
                
                <div className="mt-4 p-3 bg-blue-50 rounded">
                  <h4 className="font-semibold text-gray-700">Szczegóły:</h4>
                  <p className="text-gray-600">{tariff.details}</p>
                </div>
              </div>
            ))}
          </div>
        ) : viewMode === "metals" ? (
          <div className="bg-white p-4 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4 text-blue-800">Alokacja według metali</h2>
            <div className="flex flex-col md:flex-row gap-6">
              <div className="w-full md:w-1/2">
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <Pie
                      data={metals}
                      cx="50%"
                      cy="50%"
                      outerRadius={120}
                      dataKey="value"
                      nameKey="name"
                      label={({name, percent}) => `${(percent * 100).toFixed(0)}%`}
                    >
                      {metals.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value, name, props) => [
                      `${value}% (${formatEUR(props.payload.amount)})`,
                      name
                    ]} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              
              <div className="w-full md:w-1/2">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="bg-blue-100">
                      <th className="border border-gray-300 p-2 text-left">Metal</th>
                      <th className="border border-gray-300 p-2 text-right">Alokacja</th>
                      <th className="border border-gray-300 p-2 text-right">Kwota</th>
                    </tr>
                  </thead>
                  <tbody>
                    {metals.map((metal, index) => (
                      <tr key={index} className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                        <td className="border border-gray-300 p-2">{metal.name}</td>
                        <td className="border border-gray-300 p-2 text-right">{metal.value}%</td>
                        <td className="border border-gray-300 p-2 text-right">{formatEUR(metal.amount)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        ) : (
          <div className="bg-white p-4 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4 text-blue-800">Struktura komponentów</h2>
            <div className="flex flex-col md:flex-row gap-6">
              <div className="w-full md:w-1/2">
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={components}
                      cx="50%"
                      cy="50%"
                      outerRadius={120}
                      dataKey="value"
                      nameKey="name"
                      label={({name, value}) => `${value}%`}
                    >
                      {components.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value, name) => [`${value}% (${formatEUR(amount * value / 100)})`, name]} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              
              <div className="w-full md:w-1/2">
                <table className="w-full border-collapse">
                  <thead>
                    <tr className="bg-blue-100">
                      <th className="border border-gray-300 p-2 text-left">Komponent</th>
                      <th className="border border-gray-300 p-2 text-right">Alokacja</th>
                      <th className="border border-gray-300 p-2 text-right">Kwota</th>
                    </tr>
                  </thead>
                  <tbody>
                    {components.map((component, index) => (
                      <tr key={index} className={index % 2 === 0 ? "bg-white" : "bg-gray-50"}>
                        <td className="border border-gray-300 p-2">{component.name}</td>
                        <td className="border border-gray-300 p-2 text-right">{component.value}%</td>
                        <td className="border border-gray-300 p-2 text-right">{formatEUR(component.amount)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
        
        <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-4 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4 text-blue-800">Koszty AGIO</h2>
            <div className="flex flex-col gap-4">
              <div className="p-3 bg-yellow-50 rounded-lg border-l-4 border-yellow-400">
                <h3 className="font-medium text-gray-800">Koszt początkowy:</h3>
                <p className="mt-1 text-xl font-bold">{agio.initialPercent.toFixed(2)}% ({formatEUR(agio.initialAgio)})</p>
              </div>
              <div className="p-3 bg-green-50 rounded-lg border-l-4 border-green-400">
                <h3 className="font-medium text-gray-800">Koszt efektywny (po bonusach):</h3>
                <p className="mt-1 text-xl font-bold text-green-700">{agio.effectivePercent.toFixed(2)}% ({formatEUR(agio.effectiveAgio)})</p>
                {agio.bonus > 0 && (
                  <p className="text-sm text-green-600 mt-2">
                    <span className="font-medium">Bonus: </span> 
                    {formatEUR(agio.bonus)} zwracane w postaci dodatkowych metali
                  </p>
                )}
              </div>
            </div>
          </div>

          <div className="bg-white p-4 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4 text-blue-800">Projekcja i rekomendacja</h2>
            <div className="p-3 bg-blue-50 rounded-lg border-l-4 border-blue-400">
              <ul className="space-y-3">
                <li>
                  <span className="font-semibold">Rekomendowany depozyt: </span> 
                  <span className="text-blue-700 font-medium">{currentTariff?.name || "Brak dopasowania"}</span>
                </li>
                <li>
                  <span className="font-semibold">Efektywne AGIO: </span> 
                  <span className="text-green-700">{agio.effectivePercent.toFixed(2)}%</span>
                </li>
                <li>
                  <span className="font-semibold">Rekomendacja Efektu Kursu Średniego: </span> 
                  <span className="font-medium">{formatEUR(purchase)}/tydzień</span>
                </li>
                <li>
                  <span className="font-semibold">Roczna kwota dokupów: </span> 
                  <span className="font-medium">{formatEUR(purchase * 52)}</span>
                </li>
                <li>
                  <span className="font-semibold">Perspektywa budowy: </span> 
                  <span className="font-medium">{getYearsDisplay()} lat</span>
                </li>
                <li>
                  <span className="font-semibold">Szacowana suma po {getYearsDisplay()} latach: </span> 
                  <span className="text-blue-700 font-bold">{formatEUR(Math.round(amount + (purchase * 52 * Math.min(yearsValue, 30))))}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div className="mt-6 bg-blue-600 text-white p-4 rounded-lg shadow text-center">
          <h2 className="text-xl font-semibold mb-2">Podsumowanie strategii {strategies[strategy].name}</h2>
          <div className="space-y-2">
            <p>
              <span className="font-medium">Kwota aktywacji: </span>
              <span className="font-bold text-white">{formatEUR(Math.round(amount + agio.initialAgio))}</span>
              <span className="text-sm ml-2">({formatEUR(amount)} + {formatEUR(agio.initialAgio)} AGIO)</span>
            </p>
            <p>Szacowana alokacja środków po {getYearsDisplay()} latach: <span className="font-bold text-2xl">{formatEUR(Math.round(amount + (purchase * 52 * Math.min(yearsValue, 30))))}</span></p>
          </div>          <p className="mt-2 text-sm">Z początkowej alokacji {formatEUR(amount)} i tygodniowych dokupień w wysokości {formatEUR(purchase)}</p>
        </div>
      </div>
      
      <div className="bg-gray-200 p-4 rounded-lg mt-4 text-center text-gray-600 text-sm">
        © 2025 Kalkulator Strategii Fifty/Fifty - Narzędzie do planowania alokacji w metale | 
        <a href="https://bit.ly/m/wozniak" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:text-blue-800 ml-1">
          bit.ly/m/wozniak
        </a>
      </div>
    </div>
  );
};

export default StrategyCalculator;
