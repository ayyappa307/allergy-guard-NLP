import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  Activity, AlertTriangle, CheckCircle, ChevronRight, FileText, 
  History, Info, LogOut, Search, ShieldAlert, User, XCircle, 
  Upload, Image as ImageIcon, Check, RefreshCw, Printer, Plus,
  Sun, Moon, Stethoscope
} from "lucide-react";
import { 
  fetchAllergens, fetchSymptoms, fetchFoods, 
  registerUser, loginUser, logoutUser, 
  fetchUserLogs, assessKnownAllergies, 
  assessUnknownAllergy, getImageUrl 
} from "./api";

// 3D Parallax Tilt Card Component using Framer Motion
function TiltCard({ children, className = "", style = {}, ...props }) {
  const [rotateX, setRotateX] = useState(0);
  const [rotateY, setRotateY] = useState(0);

  function handleMouseMove(e) {
    const rect = e.currentTarget.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;
    const mouseX = e.clientX - rect.left - width / 2;
    const mouseY = e.clientY - rect.top - height / 2;
    // Calculate rotation: max 12 degrees tilt
    const rX = -(mouseY / (height / 2)) * 12;
    const rY = (mouseX / (width / 2)) * 12;
    setRotateX(rX);
    setRotateY(rY);
  }

  function handleMouseLeave() {
    setRotateX(0);
    setRotateY(0);
  }

  return (
    <motion.div
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      animate={{ rotateX, rotateY }}
      transition={{ type: "spring", stiffness: 350, damping: 20, mass: 0.4 }}
      style={{
        transformStyle: "preserve-3d",
        perspective: "1000px",
        ...style
      }}
      className={`card-3d ${className}`}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Layered 3D glassmorphic icon with drop-shadow layers
function Glass3DIcon({ icon: Icon, colorClass = "from-clinical-teal-500 to-clinical-blue-600" }) {
  return (
    <div className="relative w-14 h-14 flex items-center justify-center preserve-3d group">
      {/* 3D shadow/glow layers */}
      <div className="absolute inset-0 rounded-2xl bg-slate-200 dark:bg-slate-800 translate-z-[-10px] opacity-40 blur-[2px] transition-transform group-hover:translate-z-[-14px]" />
      <div className="absolute inset-0 rounded-2xl bg-slate-300 dark:bg-slate-700 translate-z-[-5px] opacity-60 transition-transform group-hover:translate-z-[-8px]" />
      <div className={`absolute inset-0 rounded-2xl bg-gradient-to-br ${colorClass} translate-z-0 flex items-center justify-center shadow-md border border-white/20 dark:border-slate-700/30 transition-all group-hover:scale-105 group-hover:shadow-lg`}>
        <Icon className="w-6 h-6 text-white drop-shadow-[0_2px_4px_rgba(0,0,0,0.25)]" />
      </div>
    </div>
  );
}

function Floating3DPlate() {
  return (
    <div className="relative w-48 h-40 mx-auto flex items-center justify-center perspective-[1000px] select-none pointer-events-none mb-4">
      {/* 3D saucer base plate glowing shadow */}
      <div className="absolute w-32 h-12 rounded-full bg-teal-500/10 dark:bg-teal-400/20 blur-xl transform translate-y-10 rotate-x-[75deg] animate-pulse" />

      {/* Floating 3D plate container */}
      <motion.div
        animate={{
          y: [0, -6, 0],
          rotateX: [18, 22, 18],
          rotateY: [-5, 5, -5]
        }}
        transition={{
          duration: 6,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        className="w-36 h-18 rounded-full bg-gradient-to-tr from-white/10 to-white/40 dark:from-slate-800/10 dark:to-slate-800/40 border border-white/40 dark:border-slate-700/40 shadow-xl relative flex items-center justify-center preserve-3d rotate-x-[65deg]"
      >
        {/* Inner plate rim ring */}
        <div className="absolute w-[85%] h-[85%] rounded-full border border-dashed border-white/50 dark:border-slate-600/50" />
      </motion.div>

      {/* Floating Glassmorphic Spheres above the saucer */}
      <div className="absolute inset-0 flex items-center justify-center">
        
        {/* Sphere 1: Peanut */}
        <motion.div
          animate={{
            y: [-20, -32, -20],
            x: [22, 15, 22],
            rotate: [0, 360]
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute w-8 h-8 rounded-full bg-white/25 dark:bg-slate-800/40 border border-white/60 dark:border-slate-700/60 backdrop-blur-md flex items-center justify-center shadow-md"
        >
          <span className="text-sm">🥜</span>
        </motion.div>

        {/* Sphere 2: Wheat (Gluten) */}
        <motion.div
          animate={{
            y: [10, -5, 10],
            x: [-35, -25, -35],
            rotate: [360, 0]
          }}
          transition={{
            duration: 9,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute w-8 h-8 rounded-full bg-white/25 dark:bg-slate-800/40 border border-white/60 dark:border-slate-700/60 backdrop-blur-md flex items-center justify-center shadow-md"
        >
          <span className="text-sm">🌾</span>
        </motion.div>

        {/* Sphere 3: Milk */}
        <motion.div
          animate={{
            y: [-10, -25, -10],
            x: [42, 32, 42],
            rotate: [0, 360]
          }}
          transition={{
            duration: 7,
            repeat: Infinity,
            ease: "easeInOut"
          }}
          className="absolute w-8 h-8 rounded-full bg-white/25 dark:bg-slate-800/40 border border-white/60 dark:border-slate-700/60 backdrop-blur-md flex items-center justify-center shadow-md"
        >
          <span className="text-sm">🥛</span>
        </motion.div>

        {/* Sphere 4: Drop/Liquid */}
        <motion.div
          animate={{
            y: [18, 8, 18],
            x: [10, 15, 10]
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
            delay: 1.5
          }}
          className="absolute w-7 h-7 rounded-full bg-white/25 dark:bg-slate-800/40 border border-white/60 dark:border-slate-700/60 backdrop-blur-md flex items-center justify-center shadow-md"
        >
          <span className="text-xs">💧</span>
        </motion.div>

      </div>
    </div>
  );
}

export default function App() {
  const [theme, setTheme] = useState(localStorage.getItem("allergyguard_theme") || "light");
  const [activeTab, setActiveTab] = useState("home");

  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("allergyguard_theme", theme);
  }, [theme]);

  const [allergens, setAllergens] = useState([]);
  const [symptoms, setSymptoms] = useState([]);
  const [foods, setFoods] = useState([]);
  
  // Auth state
  const [userToken, setUserToken] = useState(localStorage.getItem("allergyguard_token"));
  const [userEmail, setUserEmail] = useState(localStorage.getItem("allergyguard_email"));
  const [userName, setUserName] = useState(localStorage.getItem("allergyguard_name") || "");
  const [authEmail, setAuthEmail] = useState("");
  const [authPassword, setAuthPassword] = useState("");
  const [authName, setAuthName] = useState("");
  const [authMode, setAuthMode] = useState("login"); // login | register
  const [authError, setAuthError] = useState("");

  // Common Loading State
  const [isLoadingData, setIsLoadingData] = useState(true);

  // Known Allergy Module State
  const [knownSearch, setKnownSearch] = useState("");
  const [selectedKnownAllergens, setSelectedKnownAllergens] = useState([]);
  const [knownAssessment, setKnownAssessment] = useState(null);
  const [isAssessingKnown, setIsAssessingKnown] = useState(false);
  const [activeKnownStep, setActiveKnownStep] = useState(0);

  // Unknown Allergy Module State
  const [selectedFoodId, setSelectedFoodId] = useState("");
  const [foodSearchText, setFoodSearchText] = useState("");
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [symptomSearchText, setSymptomSearchText] = useState("");
  const [freeTextDesc, setFreeTextDesc] = useState("");
  const [uploadedPhoto, setUploadedPhoto] = useState(null);
  const [photoPreview, setPhotoPreview] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanStep, setScanStep] = useState(0);
  const [unknownAssessment, setUnknownAssessment] = useState(null);
  const [activeStep, setActiveStep] = useState(0); // Results Stepper: 0: Assessment, 1: Likely Allergen, 2: Doctor's Note, 3: Food Guidance, 4: Medicine Guidance, 5: EHR Report Card
  const [addedAllergenId, setAddedAllergenId] = useState(null); // Feedback for allergen added

  // History state
  const [historyLogs, setHistoryLogs] = useState([]);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  // Ref for autocomplete dropdown
  const [showFoodDropdown, setShowFoodDropdown] = useState(false);
  const foodInputRef = useRef(null);

  // Unique report details
  const [reportId, setReportId] = useState("");
  const [reportDate, setReportDate] = useState("");
  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");
  const [patientGender, setPatientGender] = useState("");

  // Fetch initial datasets
  useEffect(() => {
    async function loadData() {
      try {
        const [a, s, f] = await Promise.all([
          fetchAllergens(),
          fetchSymptoms(),
          fetchFoods()
        ]);
        setAllergens(a);
        setSymptoms(s);
        setFoods(f);
      } catch (err) {
        console.error("Failed to load static datasets:", err);
      } finally {
        setIsLoadingData(false);
      }
    }
    loadData();
  }, []);

  // Load history if logged in
  useEffect(() => {
    if (userToken) {
      loadHistory();
    }
  }, [userToken]);

  // Load known allergens assessment initially when allergens are loaded
  useEffect(() => {
    if (allergens.length > 0 && selectedKnownAllergens.length > 0) {
      handleKnownAssess(selectedKnownAllergens);
    }
  }, [allergens]);

  async function loadHistory() {
    setIsLoadingHistory(true);
    try {
      const logs = await fetchUserLogs();
      setHistoryLogs(logs);
    } catch (err) {
      console.error("Failed to load history:", err);
    } finally {
      setIsLoadingHistory(false);
    }
  }

  // Handle Authentication
  async function handleAuth(e) {
    e.preventDefault();
    setAuthError("");
    try {
      let data;
      if (authMode === "login") {
        data = await loginUser(authEmail, authPassword);
      } else {
        data = await registerUser(authName, authEmail, authPassword);
      }
      setUserToken(data.token);
      setUserEmail(data.email);
      setUserName(data.name || "");
      setAuthEmail("");
      setAuthPassword("");
      setAuthName("");
      setActiveTab("home");
    } catch (err) {
      setAuthError(err.message || "Authentication failed");
    }
  }


  function handleLogout() {
    logoutUser();
    setUserToken(null);
    setUserEmail(null);
    setUserName("");
    setHistoryLogs([]);
  }

  // Known Allergy Assessment
  async function handleKnownAssess(allergenIds) {
    setIsAssessingKnown(true);
    try {
      const res = await assessKnownAllergies(allergenIds);
      setKnownAssessment(res);
      // Generate report metadata if it doesn't exist
      if (allergenIds.length > 0) {
        const randomId = Math.floor(100000 + Math.random() * 900000);
        setReportId(`AG-KNOWN-${new Date().getFullYear()}-${randomId}`);
        setReportDate(new Date().toLocaleString());
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsAssessingKnown(false);
    }
  }

  // Add Allergen to Known Profile from Assessment Results
  function addAllergenToProfile(allergenId) {
    if (selectedKnownAllergens.includes(allergenId)) return;
    const next = [...selectedKnownAllergens, allergenId];
    setSelectedKnownAllergens(next);
    handleKnownAssess(next);
    setAddedAllergenId(allergenId);
    setTimeout(() => setAddedAllergenId(null), 3000);
  }

  // Unknown Allergy Form Submission
  async function handleUnknownSubmit(e) {
    e.preventDefault();
    if (!selectedFoodId && !foodSearchText && selectedSymptoms.length === 0 && !symptomSearchText && !freeTextDesc && !uploadedPhoto) {
      alert("Please provide at least one food, symptom, text description, or reaction photo.");
      return;
    }

    // Generate unique report metadata for this assessment
    const randomId = Math.floor(100000 + Math.random() * 900000);
    setReportId(`AG-${new Date().getFullYear()}-${randomId}`);
    setReportDate(new Date().toLocaleString());

    // Trigger Scanning Animation
    setIsScanning(true);
    setScanStep(0);
    setUnknownAssessment(null);

    // Scanning messages sequence
    const steps = [
      "Extracting text details with spaCy NLP...",
      "Analyzing skin reaction color histograms...",
      "Cross-referencing symptom mapping matrices...",
      "Running academic risk assessment scoring..."
    ];

    let current = 0;
    const interval = setInterval(() => {
      current++;
      if (current < steps.length) {
        setScanStep(current);
      } else {
        clearInterval(interval);
        submitUnknownAllergyData();
      }
    }, 800);
  }

  async function submitUnknownAllergyData() {
    try {
      const formData = new FormData();
      if (selectedFoodId) formData.append("food_id", selectedFoodId);
      if (foodSearchText) formData.append("food_text", foodSearchText);
      
      // Inject user's known allergies into the assessment context so the backend could reference it
      // For this local mock schema, we feed known allergy IDs into the form to weight them
      const symptomsPayload = [...selectedSymptoms];
      formData.append("symptoms", JSON.stringify(symptomsPayload));
      
      // Concat symptom text and free text description
      const fullSymptomText = [
        symptomSearchText, 
        freeTextDesc,
        selectedKnownAllergens.length > 0 ? `Patient has known allergies to: ${selectedKnownAllergens.join(", ")}` : ""
      ].filter(Boolean).join(". ");
      
      if (fullSymptomText) formData.append("symptom_text", fullSymptomText);
      
      if (uploadedPhoto) {
        formData.append("photo", uploadedPhoto);
      }

      const res = await assessUnknownAllergy(formData);
      setUnknownAssessment(res);
      setActiveStep(0); // Reset stepper to first tab
      loadHistory(); // Refresh profile logs
    } catch (err) {
      alert("Assessment failed: " + err.message);
    } finally {
      setIsScanning(false);
    }
  }

  // Handle Photo Drop
  function handlePhotoChange(e) {
    const file = e.target.files[0];
    if (file) {
      setUploadedPhoto(file);
      setPhotoPreview(URL.createObjectURL(file));
    }
  }

  function resetUnknownForm() {
    setSelectedFoodId("");
    setFoodSearchText("");
    setSelectedSymptoms([]);
    setSymptomSearchText("");
    setFreeTextDesc("");
    setUploadedPhoto(null);
    setPhotoPreview(null);
    setUnknownAssessment(null);
  }

  // Filter lists based on search
  const filteredAllergens = allergens.filter(a => 
    a.name.toLowerCase().includes(knownSearch.toLowerCase())
  );

  // Group symptoms
  const moderateSymptoms = symptoms.filter(s => s.severity === "Moderate");
  const severeSymptoms = symptoms.filter(s => s.severity === "Severe-Critical");

  // Autocomplete food filtering
  const filteredFoods = foods.filter(f => 
    f.name.toLowerCase().includes(foodSearchText.toLowerCase())
  );

  // Check if any selected symptom is severe
  const hasSevereSelected = selectedSymptoms.some(sId => {
    const sym = symptoms.find(s => s.id === sId);
    return sym && sym.severity === "Severe-Critical";
  });
  return (
    <div className="min-h-screen flex flex-col justify-between relative overflow-hidden z-10 transition-colors duration-500 bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100">
      {/* 3D ambient floating background blobs */}
      <div className="absolute top-[10%] left-[-15%] w-[45rem] h-[45rem] rounded-full blur-[120px] pointer-events-none animate-blob-slow -z-10 print:hidden transition-colors duration-500 bg-clinical-teal-500/5 dark:bg-clinical-teal-500/10" />
      <div className="absolute bottom-[10%] right-[-15%] w-[50rem] h-[50rem] rounded-full blur-[120px] pointer-events-none animate-blob-slower -z-10 print:hidden transition-colors duration-500 bg-clinical-blue-500/5 dark:bg-clinical-blue-500/10" />
      
      {/* 1. Academic Disclaimer Banner */}
      <div className="bg-gradient-to-r from-amber-500/10 to-amber-600/10 border-b border-amber-500/20 py-2 px-4 text-center print:hidden">
        <p className="text-xs text-amber-800 font-medium flex items-center justify-center gap-1.5">
          <ShieldAlert className="w-3.5 h-3.5 text-amber-700" />
          <span>ACADEMIC PROJECT: This assistant uses NLP & computer vision stubs for educational demonstration only. Not a medical device.</span>
        </p>
      </div>

      {/* 2. Emergency Banner (Visually Overrides Everything) */}
      <AnimatePresence>
        {((unknownAssessment && unknownAssessment.emergency_alert) || hasSevereSelected) && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="pulse-emergency-banner bg-rose-600 text-white font-bold py-3.5 px-6 shadow-lg text-center flex flex-col md:flex-row items-center justify-center gap-2.5 z-50 sticky top-0 print:hidden"
          >
            <AlertTriangle className="w-6 h-6 animate-bounce text-white" />
            <div>
              <span className="uppercase tracking-wider text-sm md:text-base font-extrabold block md:inline mr-2">Severe Symptoms Detected!</span>
              <span className="text-xs md:text-sm font-medium">Difficulty breathing, severe swelling, or lightheadedness are life-threatening anaphylaxis indicators. Please call emergency services (911 / 108 / 112) immediately.</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* 3. Main Header */}
      <header className="backdrop-blur-md border-b sticky top-0 z-40 shadow-sm print:hidden transition-colors duration-500 bg-white/80 dark:bg-slate-900/80 border-slate-100 dark:border-slate-800 text-slate-800 dark:text-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          
          <div className="flex items-center gap-2.5 cursor-pointer" onClick={() => setActiveTab("home")}>
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-clinical-teal-500 to-clinical-blue-600 flex items-center justify-center shadow-md">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="text-xl font-bold tracking-tight transition-colors text-slate-800 dark:text-white">Allergy<span className="text-clinical-teal-600">Guard</span></span>
              <span className="text-[10px] text-slate-400 font-semibold block uppercase tracking-wider leading-none">Health-Tech NLP+CV</span>
            </div>
          </div>

          <nav className="hidden md:flex items-center gap-6">
            <button 
              onClick={() => setActiveTab("home")}
              className={`text-sm font-medium transition-colors ${activeTab === "home" ? "text-clinical-teal-600 font-semibold" : "text-slate-500 hover:text-slate-800 dark:text-slate-300 dark:hover:text-white"}`}
            >
              Home
            </button>
            <button 
              onClick={() => setActiveTab("known")}
              className={`text-sm font-medium transition-colors ${activeTab === "known" ? "text-clinical-teal-600 font-semibold" : "text-slate-500 hover:text-slate-800 dark:text-slate-300 dark:hover:text-white"}`}
            >
              Known Allergies
            </button>
            <button 
              onClick={() => setActiveTab("unknown")}
              className={`text-sm font-medium transition-colors ${activeTab === "unknown" ? "text-clinical-teal-600 font-semibold" : "text-slate-500 hover:text-slate-800 dark:text-slate-300 dark:hover:text-white"}`}
            >
              Unknown Allergies
            </button>
            <button 
              onClick={() => setActiveTab("profile")}
              className={`text-sm font-medium transition-colors ${activeTab === "profile" ? "text-clinical-teal-600 font-semibold" : "text-slate-500 hover:text-slate-800 dark:text-slate-300 dark:hover:text-white"}`}
            >
              History & Profile
            </button>
            <button 
              onClick={() => setActiveTab("about")}
              className={`text-sm font-medium transition-colors ${activeTab === "about" ? "text-clinical-teal-600 font-semibold" : "text-slate-500 hover:text-slate-800 dark:text-slate-300 dark:hover:text-white"}`}
            >
              About
            </button>
          </nav>

          <div className="flex items-center gap-3">
            {/* 3D Theme Switch slider */}
            <button
              type="button"
              onClick={() => setTheme(t => t === "light" ? "dark" : "light")}
              className="w-14 h-7 rounded-full p-0.5 cursor-pointer relative transition-colors duration-500 flex items-center justify-between border bg-slate-100 dark:bg-slate-950 border-slate-200 dark:border-slate-700/80 shadow-[inset_0_2px_4px_rgba(0,0,0,0.1)] dark:shadow-[inset_0_2px_4px_rgba(0,0,0,0.6)]"
              title="Toggle Light/Dark Theme"
            >
              <div className="z-10 w-5 h-5 flex items-center justify-center text-amber-500 pl-1">
                <Sun className="w-3.5 h-3.5" />
              </div>
              <div className="z-10 w-5 h-5 flex items-center justify-center text-clinical-blue-400 pr-1">
                <Moon className="w-3.5 h-3.5" />
              </div>
              {/* Glassmorphic sliding knob */}
              <motion.div 
                layout
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
                className="absolute top-0.5 w-6 h-6 rounded-full shadow-md backdrop-blur-md transition-all duration-500 left-0.5 dark:left-[30px] bg-white dark:bg-gradient-to-br dark:from-indigo-500 dark:to-indigo-600 border border-slate-100 dark:border-indigo-400/30"
              />
            </button>

            {userToken ? (
              <div className="flex items-center gap-2">
                <span className="hidden sm:inline text-xs font-medium text-slate-500 dark:text-slate-400">{userEmail}</span>
                <button 
                  onClick={handleLogout}
                  className="p-1.5 rounded-lg border border-slate-200 dark:border-slate-750 hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-350 hover:text-rose-600 dark:hover:text-rose-400 transition-colors"
                  title="Logout"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <button 
                onClick={() => setActiveTab("profile")}
                className="text-xs bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-750 font-semibold text-slate-700 dark:text-slate-200 py-1.5 px-3 rounded-lg transition-colors flex items-center gap-1.5"
              >
                <User className="w-3.5 h-3.5" />
                <span>Sign In</span>
              </button>
            )}
          </div>

        </div>
      </header>

      {/* 4. Active Tab Content */}
      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 print:p-0">
        
        {isLoadingData ? (
          <div className="h-[400px] flex flex-col items-center justify-center gap-3 print:hidden">
            <RefreshCw className="w-8 h-8 text-clinical-teal-500 animate-spin" />
            <p className="text-slate-500 text-sm font-medium">Loading AllergyGuard Knowledge bases...</p>
          </div>
        ) : (
          <AnimatePresence mode="wait">
            
            {/* --- TAB: HOME --- */}
            {activeTab === "home" && (
              <motion.div 
                key="home"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                className="space-y-16 print:hidden"
              >
                
                {/* Hero Section: 2-Column Split Layout matching the mockup - OPEN AND PREMIUM */}
                <div className="grid md:grid-cols-12 gap-8 items-center max-w-7xl mx-auto py-16 px-6 md:px-12">
                  
                  {/* Left Column: Hero Text */}
                  <div className="md:col-span-7 text-left space-y-6">
                    <h1 className="text-4xl md:text-6xl font-semibold leading-tight tracking-tight text-slate-900 dark:text-white transition-colors duration-500">
                      Food allergy <br />
                      safety app
                    </h1>
                    <p className="text-base md:text-lg font-normal leading-relaxed max-w-xl text-slate-600 dark:text-slate-350 transition-colors duration-500">
                      A smart clinical exposure assessment system powered by natural language processing and computer vision triggers.
                    </p>
                    
                    <div className="pt-3">
                      <button 
                        onClick={() => setActiveTab("unknown")}
                        className="bg-gradient-to-r from-clinical-teal-500 to-clinical-teal-600 hover:from-clinical-teal-600 hover:to-clinical-teal-700 text-white font-bold text-sm py-3 px-6 rounded-full shadow-md hover:shadow-lg transition-all hover:-translate-y-0.5"
                      >
                        Learn more
                      </button>
                    </div>
                  </div>

                  {/* Right Column: Floating 3D Plate */}
                  <div className="md:col-span-5 flex justify-center items-center relative">
                    <Floating3DPlate />
                  </div>

                </div>

                {/* Cards Section: Side-by-Side 2-Column Grid - OPEN AND PREMIUM */}
                <div className="grid md:grid-cols-2 gap-8 max-w-7xl mx-auto px-6 md:px-12 pb-16">
                  
                  {/* Card 1: Known Allergies */}
                  <TiltCard 
                    onClick={() => setActiveTab("known")}
                    className="relative group cursor-pointer flex items-center justify-between p-6 rounded-2xl border transition-all duration-500 min-h-[120px] bg-white/70 dark:bg-slate-900/60 border-clinical-teal-200 dark:border-clinical-teal-500/30 shadow-sm shadow-clinical-teal-500/5 dark:shadow-[0_0_20px_rgba(20,184,166,0.1)] hover:border-clinical-teal-400 dark:hover:border-clinical-teal-400/50"
                  >
                    <div className="space-y-2 text-left pr-4">
                      <h3 className="text-xl md:text-2xl font-semibold text-slate-800 dark:text-white">Known Allergy</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 font-medium leading-normal">
                        {theme === "dark" ? "Liteo your allergen agpe in your health." : "Help your allergen agprs in your health."}
                      </p>
                    </div>
                    {/* Layered 3D Icon */}
                    <div className="flex-shrink-0">
                      {theme === "dark" ? (
                        <Glass3DIcon icon={Stethoscope} colorClass="from-clinical-teal-400 to-clinical-teal-600" />
                      ) : (
                        <div className="w-10 h-10 bg-rose-100 rounded-xl flex items-center justify-center text-rose-500 font-bold text-xl shadow-inner animate-pulse">💊</div>
                      )}
                    </div>
                  </TiltCard>
 
                  {/* Card 2: Unknown Allergies */}
                  <TiltCard 
                    onClick={() => setActiveTab("unknown")}
                    className="relative group cursor-pointer flex items-center justify-between p-6 rounded-2xl border transition-all duration-500 min-h-[120px] bg-white/70 dark:bg-slate-900/60 border-rose-200 dark:border-rose-500/30 shadow-sm shadow-rose-500/5 dark:shadow-[0_0_20px_rgba(244,63,94,0.1)] hover:border-rose-400 dark:hover:border-rose-400/50"
                  >
                    <div className="space-y-2 text-left pr-4">
                      <h3 className="text-xl md:text-2xl font-semibold text-slate-800 dark:text-white">Unknown Allergy</h3>
                      <p className="text-sm text-slate-500 dark:text-slate-400 font-medium leading-normal">
                        {theme === "dark" ? "Know your allergy's portitles to your healthcare-tech." : "Find your allergen deritles to your hover-lift."}
                      </p>
                    </div>
                    {/* Layered 3D Icon */}
                    <div className="flex-shrink-0">
                      <Glass3DIcon icon={ShieldAlert} colorClass="from-rose-400 to-rose-600" />
                    </div>
                  </TiltCard>
                </div>
              </motion.div>
            )}

            {/* --- TAB: KNOWN ALLERGIES --- */}
            {activeTab === "known" && (
              <motion.div 
                key="known"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                className="space-y-8 print:hidden"
              >
                <div className="border-b border-slate-100 dark:border-slate-800 pb-5">
                  <h2 className="text-2xl md:text-3xl font-semibold text-slate-900 dark:text-white transition-colors duration-500">Known Allergy Screening</h2>
                  <p className="text-base text-slate-500 dark:text-slate-400 leading-relaxed font-normal mt-1 transition-colors duration-500">Identify allergens to verify safe foods and local alternatives in Andhra/Telangana cuisine.</p>
                </div>

                <div className="grid lg:grid-cols-12 gap-8">
                  
                  {/* Left Column: Allergen Checklist */}
                  <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-4 transition-colors duration-500">
                    
                    {/* Patient Details Card */}
                    <div className="bg-slate-50 dark:bg-slate-950 border border-slate-200/60 dark:border-slate-800/80 rounded-xl p-4 space-y-3.5 shadow-2xs transition-colors duration-500">
                      <span className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Patient Demographics</span>
                      <div className="space-y-2.5">
                        <div>
                          <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 block mb-1">Full Name</label>
                          <input 
                            type="text"
                            placeholder="e.g. John Doe"
                            value={patientName}
                            onChange={e => setPatientName(e.target.value)}
                            className="w-full text-xs border border-slate-200 dark:border-slate-700 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-clinical-teal-500 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500"
                          />
                        </div>
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 block mb-1">Age</label>
                            <input 
                              type="number"
                              min="0"
                              max="120"
                              placeholder="e.g. 28"
                              value={patientAge}
                              onChange={e => setPatientAge(e.target.value)}
                              className="w-full text-xs border border-slate-200 dark:border-slate-700 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-clinical-teal-500 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500"
                            />
                          </div>
                          <div>
                            <label className="text-[10px] font-bold text-slate-500 dark:text-slate-400 block mb-1">Gender</label>
                            <select
                              value={patientGender}
                              onChange={e => setPatientGender(e.target.value)}
                              className="w-full text-xs border border-slate-200 dark:border-slate-700 rounded-lg px-2.5 py-1.5 focus:outline-none focus:border-clinical-teal-500 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500"
                            >
                              <option value="">Select...</option>
                              <option value="Male">Male</option>
                              <option value="Female">Female</option>
                              <option value="Other">Other</option>
                              <option value="Prefer not to say">Prefer not to say</option>
                            </select>
                          </div>
                        </div>
                      </div>
                    </div>

                    <div className="relative">
                      <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                      <input 
                        type="text"
                        placeholder="Search 25 allergens..."
                        value={knownSearch}
                        onChange={e => setKnownSearch(e.target.value)}
                        className="w-full pl-9 pr-4 py-2 border border-slate-200 dark:border-slate-700 rounded-xl text-sm focus:outline-none focus:border-clinical-teal-500 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500"
                      />
                    </div>

                    <div className="max-h-[500px] overflow-y-auto space-y-2 pr-1">
                      {filteredAllergens.map(a => {
                        const isChecked = selectedKnownAllergens.includes(a.id);
                        return (
                          <div 
                            key={a.id}
                            onClick={() => {
                              const next = isChecked 
                                ? selectedKnownAllergens.filter(x => x !== a.id) 
                                : [...selectedKnownAllergens, a.id];
                              setSelectedKnownAllergens(next);
                              handleKnownAssess(next);
                            }}
                            className={`flex items-center gap-3 p-2 rounded-xl border cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-850 transition-all ${isChecked ? "border-clinical-teal-500 bg-clinical-teal-50/30 dark:bg-clinical-teal-500/10" : "border-slate-100 dark:border-slate-800/60"}`}
                          >
                            {/* Make allergen thumbnail mini as requested */}
                            <img 
                              src={getImageUrl(a.thumbnail_path)} 
                              alt={a.name}
                              className="w-7 h-7 rounded-md object-cover bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex-shrink-0"
                            />
                            <div className="flex-grow">
                              <span className="text-xs font-bold text-slate-700 dark:text-slate-250 block">{a.name}</span>
                            </div>
                            <div className={`w-4 h-4 rounded border flex items-center justify-center transition-colors ${isChecked ? "bg-clinical-teal-500 border-clinical-teal-500 text-white" : "border-slate-300 dark:border-slate-700"}`}>
                              {isChecked && <Check className="w-3 h-3 stroke-[3]" />}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Right Column: Assessment Results Stepper */}
                  <div className={`${knownAssessment ? "lg:col-span-12 max-w-5xl mx-auto w-full" : "lg:col-span-7"} space-y-6`}>
                    {selectedKnownAllergens.length === 0 ? (
                      <div className="h-[300px] bg-slate-50 dark:bg-slate-900/40 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl flex flex-col items-center justify-center text-center p-6 space-y-3 transition-colors duration-500">
                        <Info className="w-8 h-8 text-slate-400 dark:text-slate-500" />
                        <div>
                          <p className="font-bold text-slate-700 dark:text-slate-200">No allergens selected</p>
                          <p className="text-xs text-slate-400 dark:text-slate-500 max-w-sm">Please select one or more allergens from the checklist to query safe dishes, warnings, and alternatives.</p>
                        </div>
                      </div>
                    ) : knownAssessment ? (
                      <div className="space-y-6">
                        
                        {/* Summary Bar */}
                        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-5 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-3xl shadow-sm gap-4 transition-colors duration-500">
                          <div>
                            <h3 className="text-base font-bold text-slate-800 dark:text-white">Active Assessment Results</h3>
                            <p className="text-xs text-slate-500 dark:text-slate-400 font-semibold mt-0.5">Showing warning metrics for selected allergens</p>
                          </div>
                          <button
                            type="button"
                            onClick={() => setKnownAssessment(null)}
                            className="text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-850 dark:hover:bg-slate-750 dark:text-slate-200 px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-750 transition-all cursor-pointer hover:shadow-xs"
                          >
                            Modify Selected Allergens
                          </button>
                        </div>

                        {/* Vertical Stepper Timeline (Screen Only) */}
                        <div className="space-y-4 print:hidden">
                          {[
                            { name: "Overview", icon: Info, summary: `${knownAssessment.selected_allergens_details?.length || 0} allergens selected` },
                            { name: "Mechanism", icon: Activity, summary: "Biological response & warning guidelines" },
                            { name: "Avoidance", icon: XCircle, summary: `${knownAssessment.unsafe_foods?.length || 0} unsafe dishes to avoid` },
                            { name: "Safe Dishes", icon: CheckCircle, summary: `${knownAssessment.safe_foods?.length || 0} regional dishes recommended` },
                            { name: "Medicines", icon: ShieldAlert, summary: "Stage A & B clinical guidance pathways" },
                            { name: "Report Card", icon: Printer, summary: "Official EHR Clinical Report Card PDF" }
                          ].map((step, idx) => {
                            const StepIcon = step.icon;
                            const isActive = activeKnownStep === idx;
                            const isCompleted = activeKnownStep > idx;
                            
                            return (
                              <div 
                                key={step.name} 
                                className={`transition-all duration-300 rounded-2xl overflow-hidden border ${
                                  isActive 
                                    ? "bg-white dark:bg-slate-900 border-clinical-teal-500/50 dark:border-clinical-teal-500/30 shadow-md ring-2 ring-clinical-teal-500/5 dark:ring-clinical-teal-500/20" 
                                    : "bg-white/70 dark:bg-slate-900/40 border-slate-100 dark:border-slate-800 shadow-sm hover:border-slate-300 dark:hover:border-slate-700"
                                }`}
                              >
                                {/* Step Header */}
                                <button
                                  type="button"
                                  onClick={() => setActiveKnownStep(idx)}
                                  className="w-full flex items-center justify-between p-4 text-left focus:outline-none cursor-pointer hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors"
                                >
                                  <div className="flex items-center gap-3.5">
                                    <div className={`w-9 h-9 rounded-full flex items-center justify-center border transition-all duration-300 ${
                                      isActive 
                                        ? "bg-gradient-to-br from-clinical-teal-600 to-clinical-blue-600 border-clinical-teal-500 text-white shadow-sm font-bold" 
                                        : isCompleted 
                                          ? "bg-clinical-teal-50 dark:bg-clinical-teal-950/30 text-clinical-teal-600 dark:text-clinical-teal-400 border-clinical-teal-200 dark:border-clinical-teal-900/60" 
                                          : "bg-slate-50 dark:bg-slate-800 text-slate-400 dark:text-slate-500 border-slate-200 dark:border-slate-700"
                                    }`}>
                                      {isCompleted ? (
                                        <Check className="w-4 h-4 stroke-[3]" />
                                      ) : (
                                        <span className="text-xs">{idx + 1}</span>
                                      )}
                                    </div>
                                    <div>
                                      <h4 className={`text-xs font-black uppercase tracking-wider ${isActive ? "text-slate-800 dark:text-white" : "text-slate-500 dark:text-slate-400"}`}>
                                        {step.name}
                                      </h4>
                                      <span className="text-[10px] text-slate-400 font-semibold block mt-0.5">
                                        {step.summary}
                                      </span>
                                    </div>
                                  </div>
                                  
                                  <div className="flex items-center gap-2">
                                    <div className={`w-7 h-7 rounded-lg flex items-center justify-center transition-colors ${
                                      isActive ? "bg-clinical-teal-50 dark:bg-clinical-teal-950/50 text-clinical-teal-600 dark:text-clinical-teal-400" : "text-slate-300 dark:text-slate-655"
                                    }`}>
                                      <StepIcon className="w-4 h-4" />
                                    </div>
                                  </div>
                                </button>
                                
                                {/* Expanded Content Area */}
                                <AnimatePresence initial={false}>
                                  {isActive && (
                                    <motion.div
                                      initial={{ height: 0, opacity: 0 }}
                                      animate={{ height: "auto", opacity: 1 }}
                                      exit={{ height: 0, opacity: 0 }}
                                      transition={{ duration: 0.25, ease: "easeInOut" }}
                                      className="border-t border-slate-100 dark:border-slate-800"
                                    >
                                      <div className="p-5 bg-slate-50/50 dark:bg-slate-950/30">
                                        
                                        {idx === 0 && (
                                          <div className="space-y-6">
                                            <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800">Known Allergens Overview</h3>
                                            <div className="grid md:grid-cols-2 gap-5">
                                              <div className="space-y-3">
                                                <span className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Selected Allergen Profiles:</span>
                                                <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
                                                  {knownAssessment.selected_allergens_details && knownAssessment.selected_allergens_details.map(a => (
                                                    <div key={a.id} className="flex items-start gap-3 p-3 bg-white dark:bg-slate-900 rounded-xl border border-slate-100 dark:border-slate-800 shadow-xs transition-colors duration-500">
                                                      <img src={getImageUrl(a.thumbnail_path)} alt={a.name} className="w-9 h-9 rounded-md object-cover flex-shrink-0 bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700" />
                                                      <div>
                                                        <h4 className="text-xs font-bold text-slate-800 dark:text-white">{a.name}</h4>
                                                        <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-normal font-medium mt-0.5">{a.description}</p>
                                                      </div>
                                                    </div>
                                                  ))}
                                                </div>
                                              </div>
                                              
                                              <div className="bg-gradient-to-br from-clinical-teal-50/30 to-clinical-blue-50/30 dark:from-clinical-teal-950/10 dark:to-clinical-blue-950/10 border border-clinical-teal-100/50 dark:border-clinical-teal-800/40 rounded-2xl p-5 flex flex-col justify-between space-y-4 shadow-xs transition-colors duration-500">
                                                <div>
                                                  <span className="text-[10px] font-bold text-clinical-teal-700 dark:text-clinical-teal-400 uppercase tracking-wider block">Active Profile Details</span>
                                                  <p className="text-xs text-slate-600 dark:text-slate-350 font-semibold mt-1">
                                                    We matched your active known allergy profiles against Andhra & Telangana regional dishes.
                                                  </p>
                                                </div>
                                                <div className="grid grid-cols-2 gap-3">
                                                  <div className="bg-white dark:bg-slate-900 border border-rose-100 dark:border-rose-950/50 rounded-xl p-3 text-center shadow-xs transition-colors duration-500">
                                                    <span className="text-lg font-black text-rose-600 block">{knownAssessment.unsafe_foods.length}</span>
                                                    <span className="text-[9px] text-rose-500 dark:text-rose-455 font-bold uppercase tracking-wider block">Avoid (Unsafe)</span>
                                                  </div>
                                                  <div className="bg-white dark:bg-slate-900 border border-clinical-teal-100 dark:border-clinical-teal-950/50 rounded-xl p-3 text-center shadow-xs transition-colors duration-500">
                                                    <span className="text-lg font-black text-clinical-teal-600 block">{knownAssessment.safe_foods.length}</span>
                                                    <span className="text-[9px] text-clinical-teal-500 dark:text-clinical-teal-455 font-bold uppercase tracking-wider block">Safe Dishes</span>
                                                  </div>
                                                </div>
                                                <p className="text-[9px] text-slate-400 dark:text-slate-500 italic">
                                                  Disclaimer: Academic profile study — not a substitute for clinical diagnostics.
                                                </p>
                                              </div>
                                            </div>
                                          </div>
                                        )}

                                        {idx === 1 && knownAssessment.doctor_note && (
                                          <div className="space-y-4 font-medium text-xs text-slate-600 dark:text-slate-350 leading-relaxed font-semibold">
                                            <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800 flex items-center gap-2">
                                              <FileText className="w-4 h-4 text-clinical-teal-600 dark:text-clinical-teal-400" />
                                              <span>Clinical Mechanism & Educational Overview</span>
                                            </h3>
                                            <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-4 rounded-xl shadow-xs transition-colors duration-500">
                                              <span className="text-[10px] font-black uppercase text-clinical-teal-700 dark:text-clinical-teal-400 tracking-wider">Immune System Hyper-Response</span>
                                              <p className="mt-1 font-semibold text-slate-700 dark:text-slate-300">{knownAssessment.doctor_note.mechanism}</p>
                                            </div>
                                            <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-4 rounded-xl shadow-xs transition-colors duration-500">
                                              <span className="text-[10px] font-black uppercase text-amber-700 dark:text-amber-500 tracking-wider">Clinical Guidance & Symptoms</span>
                                              <ul className="list-disc list-inside space-y-1 font-semibold text-slate-700 dark:text-slate-300">
                                                {knownAssessment.doctor_note.see_doctor_bullets.map((bullet, i) => (
                                                  <li key={i}>{bullet}</li>
                                                ))}
                                              </ul>
                                            </div>
                                            <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-4 rounded-xl shadow-xs transition-colors duration-500">
                                              <span className="text-[10px] font-black uppercase text-indigo-700 dark:text-indigo-400 tracking-wider">Expected Clinical Evaluation</span>
                                              <p className="mt-1 font-semibold text-slate-700 dark:text-slate-300">{knownAssessment.doctor_note.allergist_evaluation}</p>
                                            </div>
                                            <div className="p-3 bg-rose-50 dark:bg-rose-950/20 border border-rose-100 dark:border-rose-900/40 text-rose-800 dark:text-rose-300 text-[10px] rounded-lg font-bold">
                                              ⚠️ {knownAssessment.doctor_note.disclaimer}
                                            </div>
                                          </div>
                                        )}

                                        {idx === 2 && (
                                          <div className="space-y-4">
                                            <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800">Avoidance & Safe Alternatives</h3>
                                            {knownAssessment.unsafe_foods.length > 0 ? (
                                              <div className="grid sm:grid-cols-2 gap-4">
                                                {knownAssessment.unsafe_foods.map(food => (
                                                  <div key={food.id} className="bg-white dark:bg-slate-900 border border-rose-100 dark:border-rose-950/40 rounded-xl overflow-hidden shadow-xs flex flex-col justify-between transition-colors duration-500">
                                                    <div className="h-24 bg-slate-50 dark:bg-slate-950 relative">
                                                      <img 
                                                        src={getImageUrl(food.image_path)} 
                                                        alt={food.name}
                                                        className="w-full h-full object-cover"
                                                      />
                                                      <div className="absolute top-2 right-2 bg-rose-600 text-white text-[9px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                                                        Unsafe
                                                      </div>
                                                    </div>
                                                    <div className="p-3 space-y-1">
                                                      <span className="text-xs font-bold text-slate-800 dark:text-white block">{food.name}</span>
                                                      <p className="text-[10px] text-slate-500 dark:text-slate-400 line-clamp-2 leading-relaxed font-medium">{food.description}</p>
                                                      <div className="flex flex-wrap gap-1 pt-1">
                                                        {food.triggered_allergens.map(a => (
                                                          <span key={a} className="text-[8px] font-bold bg-rose-50 dark:bg-rose-950/30 text-rose-700 dark:text-rose-350 px-1.5 py-0.5 rounded border border-rose-100 dark:border-rose-900/40 uppercase">
                                                            {a.replace("_", " ")}
                                                          </span>
                                                        ))}
                                                      </div>
                                                    </div>
                                                    <div className="bg-rose-50/50 dark:bg-rose-950/20 border-t border-rose-50 dark:border-rose-900/20 p-2 text-center">
                                                      <span className="text-[9px] text-rose-800 dark:text-rose-300 font-bold block">Safe Alternatives:</span>
                                                      <span className="text-xs text-rose-700 dark:text-rose-400 font-bold">{food.alternatives.join(", ")}</span>
                                                    </div>
                                                  </div>
                                                ))}
                                              </div>
                                            ) : (
                                              <div className="text-center py-8 text-slate-400 dark:text-slate-500 text-xs italic font-semibold">
                                                No unsafe dishes found for your allergen profile. All dishes are safe.
                                              </div>
                                            )}
                                          </div>
                                        )}

                                        {idx === 3 && (
                                          <div className="space-y-4">
                                            <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800">Recommended Safe Dishes</h3>
                                            {knownAssessment.safe_foods.length > 0 ? (
                                              <div className="grid sm:grid-cols-2 gap-4">
                                                {knownAssessment.safe_foods.map(food => (
                                                  <div key={food.id} className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-xl overflow-hidden shadow-xs flex flex-col justify-between transition-colors duration-500">
                                                    <div className="h-24 bg-slate-50 dark:bg-slate-950 relative">
                                                      <img 
                                                        src={getImageUrl(food.image_path)} 
                                                        alt={food.name}
                                                        className="w-full h-full object-cover"
                                                      />
                                                      <div className="absolute top-2 right-2 bg-clinical-teal-600 text-white text-[9px] font-bold px-2 py-0.5 rounded-full uppercase tracking-wider">
                                                        Safe
                                                      </div>
                                                    </div>
                                                    <div className="p-3 space-y-1">
                                                      <span className="text-xs font-bold text-slate-800 dark:text-white block">{food.name}</span>
                                                      <p className="text-[10px] text-slate-500 dark:text-slate-400 line-clamp-2 leading-relaxed font-medium">{food.description}</p>
                                                    </div>
                                                    <div className="bg-slate-50 dark:bg-slate-950 p-2 border-t border-slate-100 dark:border-slate-800 flex flex-wrap gap-1">
                                                      <span className="text-[8px] text-slate-400 dark:text-slate-500 font-bold block w-full">Ingredients:</span>
                                                      <span className="text-[9px] text-slate-500 dark:text-slate-400 font-semibold line-clamp-1">{food.ingredients.join(", ")}</span>
                                                    </div>
                                                  </div>
                                                ))}
                                              </div>
                                            ) : (
                                              <div className="text-center py-8 text-slate-400 dark:text-slate-500 text-xs italic font-semibold">
                                                All regional dishes are marked unsafe under your selected allergen profile.
                                              </div>
                                            )}
                                          </div>
                                        )}

                                        {idx === 4 && (
                                          <div className="space-y-4 text-xs font-semibold">
                                            <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
                                              <span>Medicine Safety Education</span>
                                              <span className="text-[9px] bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 font-bold py-0.5 px-2 rounded uppercase">No Brand names</span>
                                            </h3>
                                            <div className="p-3 bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-900/40 text-amber-800 dark:text-amber-300 font-bold leading-normal">
                                              ⚠️ {knownAssessment.medicine_guidance.disclaimer}
                                            </div>
                                            <div className="grid md:grid-cols-2 gap-5">
                                              <div className="space-y-3">
                                                <span className="text-[10px] font-black uppercase text-clinical-teal-700 dark:text-clinical-teal-400 tracking-wider block">Stage A: Over-the-Counter Relief (Mild Reactions)</span>
                                                {knownAssessment.medicine_guidance.stage_a && knownAssessment.medicine_guidance.stage_a.length > 0 ? (
                                                  <div className="space-y-2">
                                                    {knownAssessment.medicine_guidance.stage_a.map((med, i) => (
                                                      <div key={i} className="flex gap-2.5 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-2.5 rounded-xl shadow-xs transition-colors duration-500">
                                                        {med.image_path && (
                                                          <img 
                                                            src={getImageUrl(med.image_path)} 
                                                            alt={med.category} 
                                                            className="w-11 h-11 rounded-lg object-cover bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex-shrink-0"
                                                          />
                                                        )}
                                                        <div className="space-y-0.5 flex-grow">
                                                          <span className="text-xs font-bold text-slate-700 dark:text-white block">{med.category}</span>
                                                          <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-normal font-medium">{med.description}</p>
                                                          <span className="text-[8px] text-amber-700 dark:text-amber-400 font-bold block mt-0.5">Warning: {med.warning}</span>
                                                        </div>
                                                      </div>
                                                    ))}
                                                  </div>
                                                ) : (
                                                  <p className="text-xs text-slate-400 dark:text-slate-500 italic font-semibold">No specific Stage A medicines mapped.</p>
                                                )}
                                              </div>
                                              
                                              <div className="space-y-3">
                                                <span className="text-[10px] font-black uppercase text-rose-700 dark:text-rose-400 tracking-wider block">Stage B: Prescription Rescue (Severe Reactions)</span>
                                                {knownAssessment.medicine_guidance.stage_b && knownAssessment.medicine_guidance.stage_b.length > 0 ? (
                                                  <div className="space-y-2">
                                                    {knownAssessment.medicine_guidance.stage_b.map((med, i) => (
                                                      <div key={i} className="flex gap-2.5 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-2.5 rounded-xl shadow-xs transition-colors duration-500">
                                                        {med.image_path && (
                                                          <img 
                                                            src={getImageUrl(med.image_path)} 
                                                            alt={med.category} 
                                                            className="w-11 h-11 rounded-lg object-cover bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex-shrink-0"
                                                          />
                                                        )}
                                                        <div className="space-y-0.5 flex-grow">
                                                          <span className="text-xs font-bold text-slate-700 dark:text-white block">{med.category}</span>
                                                          <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-normal font-medium">{med.description}</p>
                                                          <span className="text-[8px] text-rose-700 dark:text-rose-450 font-bold block mt-0.5">Emergency Warning: {med.warning}</span>
                                                        </div>
                                                      </div>
                                                    ))}
                                                  </div>
                                                ) : (
                                                  <p className="text-xs text-slate-400 dark:text-slate-500 italic font-semibold">No specific Stage B medicines mapped.</p>
                                                )}
                                              </div>
                                            </div>
                                          </div>
                                        )}

                                        {idx === 5 && (
                                          <div className="space-y-4">
                                            <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800">Electronic Health Record</h3>
                                            
                                            {/* EHR Mini Block */}
                                            <div className="border border-slate-300 dark:border-slate-700 p-4 rounded-xl bg-white dark:bg-slate-900 space-y-3 shadow-xs text-xs transition-colors duration-500">
                                              <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
                                                <div className="flex items-center gap-2">
                                                  <Activity className="w-4 h-4 text-slate-900 dark:text-white" />
                                                  <h4 className="font-bold text-slate-900 dark:text-white uppercase">ALLERGYGUARD PROFILE ASSESSMENT</h4>
                                                </div>
                                                <div className="text-right text-[10px] font-semibold text-slate-500 dark:text-slate-400 space-y-0.5">
                                                  <div>ID: {reportId}</div>
                                                  <div>Account: {userEmail || "GUEST"}</div>
                                                  {patientName && <div>Name: <span className="font-bold text-slate-800 dark:text-slate-200">{patientName}</span></div>}
                                                  {(patientAge || patientGender) && (
                                                    <div>
                                                      {patientAge && `Age: ${patientAge}`}
                                                      {patientAge && patientGender && " | "}
                                                      {patientGender && `Gender: ${patientGender}`}
                                                    </div>
                                                  )}
                                                </div>
                                              </div>
                                              <div className="space-y-1">
                                                <span className="text-slate-400 dark:text-slate-550 font-bold block uppercase text-[9px]">Patient Allergens:</span>
                                                <span className="font-bold text-slate-800 dark:text-slate-200 text-xs">
                                                  {knownAssessment.selected_allergens_details && knownAssessment.selected_allergens_details.map(a => a.name).join(", ") || "None Selected"}
                                                </span>
                                              </div>
                                              <div className="space-y-1">
                                                <span className="text-slate-400 dark:text-slate-550 font-bold block uppercase text-[9px]">Dietary Warnings:</span>
                                                <span className="font-medium text-slate-700 dark:text-slate-300">
                                                  Avoid {knownAssessment.unsafe_foods.map(x => x.name).join(", ") || "No unsafe foods detected"}
                                                </span>
                                              </div>
                                            </div>
                                            
                                            <button
                                              type="button"
                                              onClick={() => window.print()}
                                              className="w-full flex items-center justify-center gap-1.5 text-xs font-bold bg-slate-900 dark:bg-slate-800 hover:bg-black dark:hover:bg-slate-750 text-white py-2.5 rounded-xl shadow-xs transition-colors cursor-pointer"
                                            >
                                              <Printer className="w-4 h-4" />
                                              <span>Print/Save EHR PDF Report</span>
                                            </button>
                                          </div>
                                        )}

                                        {/* Step Inner Navigation Controls */}
                                        <div className="mt-5 flex items-center justify-between pt-4 border-t border-slate-100/80 dark:border-slate-800/80">
                                          <button
                                            type="button"
                                            disabled={idx === 0}
                                            onClick={(e) => { e.stopPropagation(); setActiveKnownStep(idx - 1); }}
                                            className={`text-[10px] font-bold px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 transition-colors ${
                                              idx === 0 
                                                ? "text-slate-300 dark:text-slate-600 bg-slate-50/50 dark:bg-slate-850/50 cursor-not-allowed border-slate-100 dark:border-slate-800" 
                                                : "text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
                                            }`}
                                          >
                                            Back
                                          </button>
                                          
                                          {idx < 5 ? (
                                            <button
                                              type="button"
                                              onClick={(e) => { e.stopPropagation(); setActiveKnownStep(idx + 1); }}
                                              className="text-[10px] font-bold bg-clinical-teal-600 hover:bg-clinical-teal-700 text-white px-4 py-1.5 rounded-xl shadow-sm transition-all hover:-translate-y-0.5 cursor-pointer"
                                            >
                                              Next Step
                                            </button>
                                          ) : (
                                            <button
                                              type="button"
                                              onClick={(e) => {
                                                e.stopPropagation();
                                                setActiveKnownStep(0);
                                                setSelectedKnownAllergens([]);
                                                setKnownAssessment(null);
                                              }}
                                              className="text-[10px] font-bold bg-slate-900 dark:bg-slate-800 hover:bg-black dark:hover:bg-slate-750 text-white px-4 py-1.5 rounded-xl shadow-sm transition-all hover:-translate-y-0.5 cursor-pointer"
                                            >
                                              Reset Checklist
                                            </button>
                                          )}
                                        </div>

                                      </div>
                                    </motion.div>
                                  )}
                                </AnimatePresence>
                              </div>
                            );
                          })}
                        </div>

                        {/* Hidden Printable Report Card (Independent from screen accordion state) */}
                        <div className="hidden print:block print-report">
                          <div className="border-4 border-double border-slate-800 p-5 rounded-2xl bg-white space-y-4">
                            <div className="flex flex-col sm:flex-row items-start justify-between gap-4 pb-4 border-b-2 border-slate-800">
                              <div className="space-y-1">
                                <div className="flex items-center gap-2">
                                  <div className="w-8 h-8 rounded bg-slate-900 flex items-center justify-center text-white print:border print:border-black">
                                    <Activity className="w-5 h-5" />
                                  </div>
                                  <h2 className="text-xl font-black text-slate-900 tracking-tight uppercase">ALLERGYGUARD KNOWN PROFILE REPORT</h2>
                                </div>
                                <p className="text-xs text-slate-500 font-bold tracking-wide">ELECTRONIC HEALTH RECORD ASSESSMENT FILE</p>
                              </div>
                              
                              <div className="text-left sm:text-right text-xs font-semibold text-slate-700 space-y-1">
                                <div><span className="text-slate-400">Report ID:</span> <span className="font-bold text-slate-800">{reportId}</span></div>
                                <div><span className="text-slate-400">Date/Time:</span> <span className="font-bold text-slate-800">{reportDate}</span></div>
                                <div><span className="text-slate-400">Account:</span> <span className="font-bold text-slate-800">{userEmail || "MOCK-GUEST"}</span></div>
                              </div>
                            </div>

                            {/* Section 0: Patient Demographics */}
                            {(patientName || patientAge || patientGender) && (
                              <div className="space-y-2 no-break-print pb-3 border-b border-slate-200 text-xs">
                                <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider">Patient Demographics</h4>
                                <div className="grid grid-cols-3 gap-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100 font-semibold">
                                  <div>
                                    <span className="text-slate-400 block font-bold text-[10px] uppercase">Name</span>
                                    <span className="text-slate-800 font-bold">{patientName || "Not Specified"}</span>
                                  </div>
                                  <div>
                                    <span className="text-slate-400 block font-bold text-[10px] uppercase">Age</span>
                                    <span className="text-slate-800 font-bold">{patientAge ? `${patientAge} yrs` : "Not Specified"}</span>
                                  </div>
                                  <div>
                                    <span className="text-slate-400 block font-bold text-[10px] uppercase">Gender</span>
                                    <span className="text-slate-800 font-bold">{patientGender || "Not Specified"}</span>
                                  </div>
                                </div>
                              </div>
                            )}

                            {/* Section 1: Selected Allergens */}
                            <div className="space-y-2 no-break-print pb-3 border-b border-slate-200">
                              <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider">I. Confirmed Patient Allergens Profile</h4>
                              <div className="grid grid-cols-1 gap-2 text-xs">
                                <div>
                                  <span className="text-slate-400 block font-bold">Active Diagnosed Allergens:</span>
                                  <span className="font-bold text-slate-800 uppercase">
                                    {knownAssessment.selected_allergens_details && knownAssessment.selected_allergens_details.map(a => a.name).join(", ") || "None Selected"}
                                  </span>
                                </div>
                              </div>
                            </div>

                            {/* Section 2: Dietary Guidance */}
                            <div className="space-y-2 no-break-print pb-3 border-b border-slate-200">
                              <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider">II. Dietary Cross-Reactivity & Avoidance Details</h4>
                              {knownAssessment.unsafe_foods && knownAssessment.unsafe_foods.length > 0 ? (
                                <table className="w-full text-left text-xs border-collapse">
                                  <thead>
                                    <tr className="border-b border-slate-300">
                                      <th className="py-2 font-black text-slate-700">Dish Name</th>
                                      <th className="py-2 font-black text-slate-700">Triggering Allergen</th>
                                      <th className="py-2 font-black text-slate-700">Safe Replacement Recommendation</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    {knownAssessment.unsafe_foods.map(x => (
                                      <tr key={x.id} className="border-b border-slate-100">
                                        <td className="py-2 font-extrabold text-slate-800">{x.name}</td>
                                        <td className="py-2 text-rose-700 font-bold">{x.triggered_allergens.join(", ").replace("_", " ")}</td>
                                        <td className="py-2 text-slate-500">{x.alternatives.join(", ")}</td>
                                      </tr>
                                    ))}
                                  </tbody>
                                </table>
                              ) : (
                                <p className="text-xs italic text-slate-400">No dishes identified as unsafe.</p>
                              )}
                            </div>

                            {/* Section 3: Medicine Guidance */}
                            <div className="space-y-3 no-break-print pb-3 border-b border-slate-200">
                              <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider">III. Precautionary Medical Guidance</h4>
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs leading-normal font-medium">
                                <div className="space-y-1">
                                  <span className="text-slate-400 block font-bold">Stage A (OTC Symptom Care):</span>
                                  <p className="text-slate-600">
                                    {knownAssessment.medicine_guidance.stage_a && knownAssessment.medicine_guidance.stage_a.map(m => m.category).join(", ") || "None mapped"}
                                  </p>
                                </div>
                                <div className="space-y-1">
                                  <span className="text-slate-400 block font-bold">Stage B (Prescription Emergency):</span>
                                  <p className="text-slate-600">
                                    {knownAssessment.medicine_guidance.stage_b && knownAssessment.medicine_guidance.stage_b.map(m => m.category).join(", ") || "None mapped"}
                                  </p>
                                </div>
                              </div>
                            </div>

                            {/* Section 4: Academic Warning */}
                            <div className="pt-2 no-break-print flex flex-col items-center text-center space-y-1.5">
                              <span className="text-[10px] text-amber-800 bg-amber-500/10 font-black px-4 py-1.5 rounded-full border border-amber-500/20 uppercase tracking-wide leading-none">
                                ⚠️ ACADEMIC REFERENCE STUDY FILE — NOT FOR DIAGNOSTIC USE
                              </span>
                              <p className="text-[10px] text-slate-400 font-medium max-w-lg">
                                This EHR report represents a local data mockup generated for patient screening reference only. Confirm all clinical diagnoses and prescriptions with a certified allergist.
                              </p>
                            </div>
                          </div>
                        </div>

                      </div>
                    ) : (
                      <div className="h-[300px] flex items-center justify-center bg-white border border-slate-100 rounded-2xl shadow-sm">
                        <RefreshCw className="w-6 h-6 text-clinical-teal-500 animate-spin" />
                      </div>
                    )}
                  </div>
                </div>
              </motion.div>
            )}

            {/* --- TAB: UNKNOWN ALLERGIES --- */}
            {activeTab === "unknown" && (
              <motion.div 
                key="unknown"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                className="space-y-8"
              >
                <div className="border-b border-slate-100 dark:border-slate-800 pb-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 print:hidden">
                  <div>
                    <h2 className="text-2xl md:text-3xl font-semibold text-slate-900 dark:text-white transition-colors duration-500">Unknown Allergy Screening</h2>
                    <p className="text-base text-slate-500 dark:text-slate-400 leading-relaxed font-normal mt-1 transition-colors duration-500">Use structured checklists, free text (analyzed via NLP), and reaction photos (classified via Computer Vision) to screen risks.</p>
                  </div>
                  <button 
                    onClick={resetUnknownForm}
                    className="text-xs bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 py-1.5 px-3 rounded-lg font-semibold transition-colors flex items-center gap-1.5 self-start cursor-pointer"
                  >
                    Reset Form
                  </button>
                </div>

                {!unknownAssessment && !isScanning ? (
                  <form onSubmit={handleUnknownSubmit} className="grid lg:grid-cols-12 gap-8 print:hidden">
                    
                    {/* Left Column: Inputs */}
                    <div className="lg:col-span-7 space-y-6">

                      {/* Patient Details Card */}
                      <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3.5 transition-colors duration-500">
                        <span className="text-sm font-bold text-slate-700 dark:text-white block">Patient Demographics</span>
                        <div className="space-y-3">
                          <div>
                            <label className="text-xs font-bold text-slate-500 dark:text-slate-400 block mb-1">Full Name</label>
                            <input 
                              type="text"
                              placeholder="e.g. John Doe"
                              value={patientName}
                              onChange={e => setPatientName(e.target.value)}
                              className="w-full text-xs border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 focus:outline-none focus:border-clinical-teal-500 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500"
                            />
                          </div>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <label className="text-xs font-bold text-slate-500 dark:text-slate-400 block mb-1">Age</label>
                              <input 
                                type="number"
                                min="0"
                                max="120"
                                placeholder="e.g. 28"
                                value={patientAge}
                                onChange={e => setPatientAge(e.target.value)}
                                className="w-full text-xs border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 focus:outline-none focus:border-clinical-teal-500 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500"
                              />
                            </div>
                            <div>
                              <label className="text-xs font-bold text-slate-500 dark:text-slate-400 block mb-1">Gender</label>
                              <select
                                value={patientGender}
                                onChange={e => setPatientGender(e.target.value)}
                                className="w-full text-xs border border-slate-200 dark:border-slate-700 rounded-xl px-3 py-2 focus:outline-none focus:border-clinical-teal-500 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500"
                              >
                                <option value="">Select...</option>
                                <option value="Male">Male</option>
                                <option value="Female">Female</option>
                                <option value="Other">Other</option>
                                <option value="Prefer not to say">Prefer not to say</option>
                              </select>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      {/* Known Allergies Reference Module */}
                      <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3 transition-colors duration-500">
                        <label className="block text-sm font-bold text-slate-700 dark:text-white flex items-center gap-1">
                          <CheckCircle className="w-4 h-4 text-clinical-teal-600 dark:text-clinical-teal-400" />
                          <span>Known Allergies Profile (Clinical Reference)</span>
                        </label>
                        
                        {selectedKnownAllergens.length > 0 ? (
                          <div className="space-y-2">
                            <p className="text-xs text-slate-400 dark:text-slate-500 font-medium">The following known allergens are active on your profile and factored into the clinical scoring matrix:</p>
                            <div className="flex flex-wrap gap-1.5">
                              {selectedKnownAllergens.map(aId => {
                                const allergenName = allergens.find(a => a.id === aId)?.name || aId;
                                return (
                                  <span key={aId} className="text-xs font-bold bg-clinical-teal-50 dark:bg-clinical-teal-950/20 border border-clinical-teal-100 dark:border-clinical-teal-900/40 text-clinical-teal-800 dark:text-clinical-teal-300 px-2.5 py-1 rounded-full uppercase">
                                    {allergenName}
                                  </span>
                                );
                              })}
                            </div>
                          </div>
                        ) : (
                          <div className="text-xs text-slate-400 dark:text-slate-500 italic">
                            No known allergies configured in profile. Go to <span className="text-clinical-teal-600 dark:text-clinical-teal-400 font-bold hover:underline cursor-pointer" onClick={() => setActiveTab("known")}>Known Allergies tab</span> to select clinical diagnoses.
                          </div>
                        )}
                      </div>

                      {/* Food Selection */}
                      <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3 relative transition-colors duration-500">
                        <label className="block text-sm font-bold text-slate-700 dark:text-white">What food did you eat? (Autocomplete lookup)</label>
                        <div className="relative" ref={foodInputRef}>
                          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                          <input 
                            type="text"
                            placeholder="Type to search Andhra/Telangana dishes (e.g. Pesarattu, Biryani)..."
                            value={foodSearchText}
                            onChange={e => {
                              setFoodSearchText(e.target.value);
                              setShowFoodDropdown(true);
                            }}
                            onFocus={() => setShowFoodDropdown(true)}
                            className="w-full pl-9 pr-4 py-2.5 border border-slate-200 dark:border-slate-700 rounded-xl text-sm focus:outline-none focus:border-clinical-teal-500 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 transition-colors duration-500"
                          />
                          
                          {showFoodDropdown && foodSearchText && (
                            <div className="absolute top-12 left-0 right-0 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-xl shadow-lg max-h-60 overflow-y-auto z-50 transition-colors duration-500">
                              {filteredFoods.map(f => (
                                <div 
                                  key={f.id}
                                  onClick={() => {
                                    setSelectedFoodId(f.id);
                                    setFoodSearchText(f.name);
                                    setShowFoodDropdown(false);
                                  }}
                                  className="px-4 py-2.5 hover:bg-slate-50 dark:hover:bg-slate-800 text-sm text-slate-700 dark:text-slate-200 cursor-pointer flex items-center justify-between"
                                >
                                  <span>{f.name}</span>
                                  <span className="text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-405 font-semibold px-2 py-0.5 rounded uppercase">Dish</span>
                                </div>
                              ))}
                              {filteredFoods.length === 0 && (
                                <div className="px-4 py-3 text-xs text-slate-400 dark:text-slate-500 italic">
                                  No exact matching dish found. spaCy will parse food ingredients from the text on submit.
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Symptom Checklist with visual images (Grid Layout) */}
                      <div className="bg-white border border-slate-100 rounded-2xl p-5 shadow-sm space-y-5">
                        <label className="block text-sm font-bold text-slate-700">Identify your symptoms (Click card to select)</label>
                        
                        {/* Moderate Symptoms */}
                        <div className="space-y-3">
                          <span className="text-xs font-bold text-clinical-blue-700 uppercase tracking-wider block">Moderate Symptoms</span>
                          
                          {/* Grid with visual thumbnails */}
                          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                            {moderateSymptoms.map(s => {
                              const isChecked = selectedSymptoms.includes(s.id);
                              return (
                                <div 
                                  key={s.id}
                                  onClick={() => {
                                    setSelectedSymptoms(isChecked 
                                      ? selectedSymptoms.filter(x => x !== s.id) 
                                      : [...selectedSymptoms, s.id]
                                    );
                                  }}
                                  className={`relative flex flex-col justify-between p-2 rounded-xl border text-[11px] cursor-pointer hover:shadow-md transition-all duration-200 select-none ${isChecked ? "border-clinical-blue-500 bg-clinical-blue-50/30 ring-2 ring-clinical-blue-500/20" : "border-slate-100 bg-white"}`}
                                >
                                  <div className="h-16 w-full rounded-lg overflow-hidden bg-slate-50 border border-slate-100 mb-1.5 relative flex-shrink-0">
                                    <img 
                                      src={s.image_path ? getImageUrl(s.image_path) : "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=150&auto=format&fit=crop&q=60"} 
                                      alt={s.name} 
                                      className="w-full h-full object-cover"
                                      onError={(e) => {
                                        e.currentTarget.onerror = null;
                                        e.currentTarget.src = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=150&auto=format&fit=crop&q=60";
                                      }}
                                    />
                                    <div className={`absolute top-1 right-1 w-4 h-4 rounded-full border flex items-center justify-center transition-colors ${isChecked ? "bg-clinical-blue-600 border-clinical-blue-600 text-white" : "bg-white/90 dark:bg-slate-800 border-slate-300 dark:border-slate-750"}`}>
                                      {isChecked && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                                    </div>
                                  </div>
                                  <div className="text-center font-bold text-slate-700 dark:text-slate-350 leading-tight line-clamp-2 flex-grow flex items-center justify-center">
                                    {s.name}
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>

                        {/* Severe Symptoms */}
                        <div className="space-y-3 pt-4 border-t border-slate-100 dark:border-slate-800">
                          <span className="text-xs font-bold text-rose-700 dark:text-rose-455 uppercase tracking-wider block flex items-center gap-1">
                            <AlertTriangle className="w-3.5 h-3.5 text-rose-600 animate-bounce" />
                            <span>Severe-Critical Symptoms</span>
                          </span>
                          
                          {/* Grid with visual thumbnails */}
                          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
                            {severeSymptoms.map(s => {
                              const isChecked = selectedSymptoms.includes(s.id);
                              return (
                                <div 
                                  key={s.id}
                                  onClick={() => {
                                    setSelectedSymptoms(isChecked 
                                      ? selectedSymptoms.filter(x => x !== s.id) 
                                      : [...selectedSymptoms, s.id]
                                    );
                                  }}
                                  className={`relative flex flex-col justify-between p-2 rounded-xl border text-[11px] cursor-pointer hover:shadow-md transition-all duration-200 select-none ${isChecked ? "border-rose-500 bg-rose-50/30 ring-2 ring-rose-500/20" : "border-slate-100 dark:border-slate-800/80 bg-white dark:bg-slate-900"}`}
                                >
                                  <div className="h-16 w-full rounded-lg overflow-hidden bg-slate-50 dark:bg-slate-950 border border-slate-100 dark:border-slate-800 mb-1.5 relative flex-shrink-0">
                                    <img 
                                      src={s.image_path ? getImageUrl(s.image_path) : "https://images.unsplash.com/photo-1618005198143-e528346d9a59?w=150&auto=format&fit=crop&q=60"} 
                                      alt={s.name} 
                                      className="w-full h-full object-cover"
                                      onError={(e) => {
                                        e.currentTarget.onerror = null;
                                        e.currentTarget.src = "https://images.unsplash.com/photo-1618005198143-e528346d9a59?w=150&auto=format&fit=crop&q=60";
                                      }}
                                    />
                                    <div className={`absolute top-1 right-1 w-4 h-4 rounded-full border flex items-center justify-center transition-colors ${isChecked ? "bg-rose-600 border-rose-600 text-white" : "bg-white/90 dark:bg-slate-800 border-slate-300 dark:border-slate-750"}`}>
                                      {isChecked && <Check className="w-2.5 h-2.5 stroke-[3]" />}
                                    </div>
                                  </div>
                                  <div className="text-center font-bold text-slate-800 dark:text-slate-200 leading-tight line-clamp-2 flex-grow flex items-center justify-center">
                                    {s.name}
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>

                      </div>

                      {/* Free text symptom description */}
                      <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-3 transition-colors duration-500">
                        <label className="block text-sm font-bold text-slate-700 dark:text-white">Describe in your own words (Optional)</label>
                        <textarea 
                          rows={3}
                          placeholder="e.g. I ate moong beans and then my throat started tightening. I also feel dizzy..."
                          value={freeTextDesc}
                          onChange={e => setFreeTextDesc(e.target.value)}
                          className="w-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 rounded-xl p-3 text-sm focus:outline-none focus:border-clinical-teal-500 transition-colors duration-500"
                        />
                        <span className="text-[10px] text-slate-400 dark:text-slate-500 block font-medium">NLP Engine will extract matching dishes and symptoms from your sentence.</span>
                      </div>

                    </div>

                    {/* Right Column: Photo Upload & Action */}
                    <div className="lg:col-span-5 space-y-6">
                      
                      {/* Photo Uploader */}
                      <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-4 transition-colors duration-500">
                        <label className="block text-sm font-bold text-slate-700 dark:text-white">Add a Reaction Photo (Optional)</label>
                        
                        <div className="border-2 border-dashed border-slate-200 dark:border-slate-700 rounded-xl p-6 text-center hover:border-clinical-teal-500 transition-colors cursor-pointer relative overflow-hidden group">
                          <input 
                            type="file" 
                            accept="image/*"
                            onChange={handlePhotoChange}
                            className="absolute inset-0 opacity-0 cursor-pointer z-10"
                          />
                          
                          {photoPreview ? (
                            <div className="space-y-3">
                              <img 
                                src={photoPreview} 
                                alt="Preview" 
                                className="max-h-48 mx-auto object-cover rounded-lg border border-slate-100 dark:border-slate-800"
                              />
                              <p className="text-xs text-slate-400 dark:text-slate-550 font-semibold">Click or drag new image to replace</p>
                            </div>
                          ) : (
                            <div className="space-y-2 py-4">
                              <Upload className="w-8 h-8 text-slate-400 dark:text-slate-500 mx-auto group-hover:text-clinical-teal-600 transition-colors" />
                              <div className="text-sm font-semibold text-slate-700 dark:text-slate-300">Click or Drag & Drop Image</div>
                              <p className="text-xs text-slate-400 dark:text-slate-500 max-w-[200px] mx-auto leading-relaxed">
                                Upload a clear skin reaction photo (hives, redness, swelling) for supplementary pattern mapping.
                              </p>
                            </div>
                          )}
                        </div>
                        
                        <span className="text-[10px] text-slate-400 dark:text-slate-500 block leading-relaxed text-center font-medium">
                          Note: Visual analysis maps patterns to the symptom scoring pool only. It does not provide clinical diagnoses.
                        </span>
                      </div>

                      {/* Submit Trigger */}
                      <button 
                        type="submit"
                        className="w-full bg-gradient-to-r from-clinical-teal-600 to-clinical-blue-600 hover:from-clinical-teal-700 hover:to-clinical-blue-700 text-white font-bold text-base py-4 px-6 rounded-xl shadow-lg hover:shadow-xl transition-all flex items-center justify-center gap-2 cursor-pointer"
                      >
                        <Activity className="w-5 h-5" />
                        <span>Run Risk Assessment</span>
                      </button>

                    </div>

                  </form>
                ) : isScanning ? (
                  /* Loading Scanner Screen */
                  <div className="max-w-xl mx-auto bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-3xl p-8 shadow-xl text-center space-y-6 my-12 print:hidden transition-colors duration-500">
                    <h3 className="text-xl font-bold text-slate-800 dark:text-white">Processing Clinical Signals</h3>
                    
                    {photoPreview ? (
                      <div className="relative w-64 h-48 mx-auto overflow-hidden rounded-xl border border-slate-200 dark:border-slate-800 shadow-md">
                        <img 
                          src={photoPreview} 
                          alt="Scanning" 
                          className="w-full h-full object-cover blur-[0.5px]"
                        />
                        <div className="absolute left-0 right-0 h-1 bg-clinical-teal-500 shadow-[0_0_8px_rgba(20,184,166,0.8)] scanner-laser"></div>
                        <div className="absolute inset-0 bg-clinical-teal-900/10 dark:bg-clinical-teal-950/20 mix-blend-overlay"></div>
                      </div>
                    ) : (
                      <div className="w-16 h-16 rounded-full bg-clinical-teal-50 dark:bg-clinical-teal-950/30 flex items-center justify-center mx-auto text-clinical-teal-600 dark:text-clinical-teal-400">
                        <RefreshCw className="w-8 h-8 animate-spin" />
                      </div>
                    )}

                    <div className="space-y-2">
                      <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                        <div 
                          className="h-full bg-gradient-to-r from-clinical-teal-500 to-clinical-blue-500 transition-all duration-300"
                          style={{ width: `${(scanStep + 1) * 25}%` }}
                        ></div>
                      </div>
                      <p className="text-sm font-semibold text-clinical-teal-600 animate-pulse">
                        {scanStep === 0 && "Extracting text details with spaCy NLP..."}
                        {scanStep === 1 && "Analyzing skin reaction color histograms..."}
                        {scanStep === 2 && "Cross-referencing symptom mapping matrices..."}
                        {scanStep === 3 && "Running academic risk assessment scoring..."}
                      </p>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-6 max-w-5xl mx-auto w-full">
                    
                    {/* Summary Bar */}
                    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between p-5 bg-white border border-slate-100 dark:border-slate-800 rounded-3xl shadow-sm gap-4">
                      <div>
                        <h3 className="text-base font-bold text-slate-800 dark:text-white">Active Assessment Results</h3>
                        <p className="text-xs text-slate-500 dark:text-slate-400 font-semibold mt-0.5">Showing warning metrics from text NLP and image scan analysis</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => setUnknownAssessment(null)}
                        className="text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 dark:bg-slate-800 dark:hover:bg-slate-700 dark:text-slate-200 px-4 py-2 rounded-xl border border-slate-200 dark:border-slate-700 transition-all cursor-pointer hover:shadow-xs"
                      >
                        Modify Assessment Inputs
                      </button>
                    </div>

                    {/* Vertical Stepper Timeline (Screen Only) */}
                    <div className="space-y-4 print:hidden">
                      {[
                        { name: "Summary", icon: Info, summary: "Inputs & visual pattern mapping" },
                        { name: "Likely Allergens", icon: AlertTriangle, summary: "Likelihood triggers & profile mapping" },
                        { name: "Doctor's Note", icon: Activity, summary: "Mechanism & clinical next steps" },
                        { name: "Avoidance", icon: XCircle, summary: "Dishes & safe alternative recommendations" },
                        { name: "Medicines", icon: ShieldAlert, summary: "Stage-based medical pathways" },
                        { name: "Report Card", icon: Printer, summary: "Official EHR Clinical Report Card PDF" }
                      ].map((step, idx) => {
                        const StepIcon = step.icon;
                        const isActive = activeStep === idx;
                        const isCompleted = activeStep > idx;
                        
                        return (
                          <div 
                                          className={`transition-all duration-300 rounded-2xl overflow-hidden border ${
                              isActive 
                                ? "bg-white dark:bg-slate-900 border-clinical-blue-500/50 dark:border-clinical-blue-500/30 shadow-md ring-2 ring-clinical-blue-500/5 dark:ring-clinical-blue-500/20" 
                                : "bg-white/70 dark:bg-slate-900/40 border-slate-100 dark:border-slate-800 shadow-sm hover:border-slate-300 dark:hover:border-slate-700"
                            }`}
                          >
                            {/* Step Header */}
                            <button
                              type="button"
                              onClick={() => setActiveStep(idx)}
                              className="w-full flex items-center justify-between p-4 text-left focus:outline-none cursor-pointer hover:bg-slate-50/50 dark:hover:bg-slate-800/30 transition-colors"
                            >
                              <div className="flex items-center gap-3.5">
                                <div className={`w-9 h-9 rounded-full flex items-center justify-center border transition-all duration-300 ${
                                  isActive 
                                    ? "bg-gradient-to-br from-clinical-blue-600 to-clinical-teal-600 border-clinical-blue-500 text-white shadow-sm font-bold" 
                                    : isCompleted 
                                      ? "bg-clinical-blue-50 dark:bg-clinical-blue-950/30 text-clinical-blue-600 dark:text-clinical-blue-400 border-clinical-blue-200 dark:border-clinical-blue-900/60" 
                                      : "bg-slate-50 dark:bg-slate-800 text-slate-400 dark:text-slate-505 border-slate-200 dark:border-slate-700"
                                  }`}>
                                  {isCompleted ? (
                                    <Check className="w-4 h-4 stroke-[3]" />
                                  ) : (
                                    <span className="text-xs">{idx + 1}</span>
                                  )}
                                </div>
                                <div>
                                  <h4 className={`text-xs font-black uppercase tracking-wider ${isActive ? "text-slate-800 dark:text-white" : "text-slate-500 dark:text-slate-400"}`}>
                                    {step.name}
                                  </h4>
                                  <span className="text-[10px] text-slate-400 font-semibold block mt-0.5">
                                    {step.summary}
                                  </span>
                                </div>
                              </div>
                              
                              <div className="flex items-center gap-2">
                                <div className={`w-7 h-7 rounded-lg flex items-center justify-center transition-colors ${
                                  isActive ? "bg-clinical-blue-50 dark:bg-clinical-blue-950/50 text-clinical-blue-600 dark:text-clinical-blue-400" : "text-slate-300 dark:text-slate-655"
                                }`}>
                                  <StepIcon className="w-4 h-4" />
                                </div>
                              </div>
                            </button>
                            
                            {/* Expanded Content Area */}
                            <AnimatePresence initial={false}>
                              {isActive && (
                                <motion.div
                                  initial={{ height: 0, opacity: 0 }}
                                  animate={{ height: "auto", opacity: 1 }}
                                  exit={{ height: 0, opacity: 0 }}
                                  transition={{ duration: 0.25, ease: "easeInOut" }}
                                  className="border-t border-slate-100 dark:border-slate-800"
                                >
                                  <div className="p-5 bg-slate-50/50 dark:bg-slate-950/30">
                                    
                                    {idx === 0 && (
                                      <div className="space-y-6">
                                        <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800">Assessment Input Signals</h3>
                                        
                                        <div className="grid md:grid-cols-2 gap-5">
                                          <div className="space-y-4">
                                            <div>
                                              <span className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Target Foods Identified</span>
                                              <div className="flex flex-wrap gap-2 mt-1.5">
                                                {unknownAssessment.extracted_foods && unknownAssessment.extracted_foods.length > 0 ? (
                                                  unknownAssessment.extracted_foods.map(f => (
                                                    <span key={f} className="text-xs font-semibold bg-clinical-teal-50 dark:bg-clinical-teal-950/20 text-clinical-teal-800 dark:text-clinical-teal-300 border border-clinical-teal-100 dark:border-clinical-teal-900/40 px-3 py-1 rounded-full uppercase transition-colors duration-500">
                                                      {f.replace("_", " ")}
                                                    </span>
                                                  ))
                                                ) : selectedFoodId ? (
                                                  <span className="text-xs font-semibold bg-clinical-teal-50 dark:bg-clinical-teal-950/20 text-clinical-teal-800 dark:text-clinical-teal-300 border border-clinical-teal-100 dark:border-clinical-teal-900/40 px-3 py-1 rounded-full uppercase transition-colors duration-500">
                                                    {selectedFoodId.replace("_", " ")}
                                                  </span>
                                                ) : (
                                                  <span className="text-xs text-slate-400 dark:text-slate-500 italic font-semibold">No exact food specified in text. Using general screening parameters.</span>
                                                )}
                                              </div>
                                            </div>
 
                                            <div>
                                              <span className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Checked & Extracted Symptoms</span>
                                              <div className="flex flex-wrap gap-1.5 mt-1.5">
                                                {selectedSymptoms.map(sId => {
                                                  const sym = symptoms.find(s => s.id === sId);
                                                  const isSevere = sym?.severity === "Severe-Critical";
                                                  return (
                                                    <span key={sId} className={`text-xs font-medium px-2.5 py-1 rounded border transition-colors duration-500 ${isSevere ? "bg-rose-50 dark:bg-rose-950/20 text-rose-700 dark:text-rose-300 border-rose-100 dark:border-rose-900/40 font-bold" : "bg-clinical-blue-50 dark:bg-clinical-blue-950/20 text-clinical-blue-800 dark:text-clinical-blue-300 border-clinical-blue-100 dark:border-clinical-blue-900/40"}`}>
                                                      {sym?.name || sId}
                                                    </span>
                                                  );
                                                })}
                                                {unknownAssessment.extracted_symptoms && unknownAssessment.extracted_symptoms.map(sId => {
                                                  const sym = symptoms.find(s => s.id === sId);
                                                  if (selectedSymptoms.includes(sId)) return null;
                                                  const isSevere = sym?.severity === "Severe-Critical";
                                                  return (
                                                    <span key={sId} className={`text-xs font-medium px-2.5 py-1 rounded border border-dashed transition-colors duration-500 ${isSevere ? "bg-rose-50 dark:bg-rose-950/20 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-900/40 font-bold" : "bg-clinical-blue-50 dark:bg-clinical-blue-950/20 text-clinical-blue-800 dark:text-clinical-blue-300 border-clinical-blue-200 dark:border-clinical-blue-900/40"}`}>
                                                      {sym?.name || sId} (Extracted)
                                                    </span>
                                                  );
                                                })}
                                                {selectedSymptoms.length === 0 && (!unknownAssessment.extracted_symptoms || unknownAssessment.extracted_symptoms.length === 0) && (
                                                  <span className="text-xs text-slate-400 dark:text-slate-500 italic font-semibold">No symptoms selected.</span>
                                                )}
                                              </div>
                                            </div>
                                          </div>
 
                                          <div>
                                            <span className="text-[10px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">Visual Pattern Analysis</span>
                                            <div className="mt-2">
                                              {unknownAssessment.photo_analysis ? (
                                                <div className="bg-white dark:bg-slate-900 rounded-xl p-3 border border-slate-100 dark:border-slate-800 flex items-center gap-3.5 shadow-xs transition-colors duration-500">
                                                  {photoPreview && (
                                                    <img 
                                                      src={photoPreview} 
                                                      alt="Analyzed" 
                                                      className="w-14 h-14 rounded-lg object-cover border border-slate-200 dark:border-slate-700 shadow-sm"
                                                    />
                                                  )}
                                                  <div className="space-y-0.5">
                                                    <span className="text-[10px] font-bold text-slate-500 dark:text-slate-400 uppercase block">Visual Pattern Match:</span>
                                                    <span className="text-xs font-black text-clinical-teal-700 dark:text-clinical-teal-400 block uppercase tracking-wide">
                                                      {unknownAssessment.photo_analysis.label}
                                                    </span>
                                                    <span className="text-[10px] font-semibold text-slate-550 dark:text-slate-400 block">
                                                      Confidence: <span className="text-slate-800 dark:text-slate-200 font-bold">{(unknownAssessment.photo_analysis.confidence * 100).toFixed(0)}%</span>
                                                    </span>
                                                  </div>
                                                </div>
                                              ) : (
                                                <div className="border border-dashed border-slate-200 dark:border-slate-700 rounded-xl p-6 text-center text-xs text-slate-400 dark:text-slate-500 italic font-semibold">
                                                  No reaction photo was provided for visual pattern extraction.
                                                </div>
                                              )}
                                            </div>
                                          </div>
                                        </div>
                                      </div>
                                    )}
 
                                    {idx === 1 && (
                                      <div className="space-y-4">
                                        <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800">Top Likely Allergen Triggers</h3>
                                        {unknownAssessment.top_allergens && unknownAssessment.top_allergens.length > 0 ? (
                                          <div className="space-y-3">
                                            {unknownAssessment.top_allergens.map((allergen, index) => {
                                              const isAlreadyKnown = selectedKnownAllergens.includes(allergen.id);
                                              return (
                                                <div key={allergen.id} className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-xl p-4 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4 transition-colors duration-500">
                                                  <div className="space-y-1 flex-grow">
                                                    <div className="flex items-center gap-2">
                                                      <span className="w-5 h-5 rounded-full bg-slate-100 dark:bg-slate-800 text-[10px] font-black text-slate-600 dark:text-slate-300 flex items-center justify-center flex-shrink-0">
                                                        {index + 1}
                                                      </span>
                                                      <span className="text-xs font-bold text-slate-800 dark:text-white">{allergen.name}</span>
                                                    </div>
                                                    <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-normal pl-7 font-medium">
                                                      {allergen.description}
                                                    </p>
                                                  </div>
                                                  
                                                  <div className="flex items-center gap-3.5 justify-between pl-7 sm:pl-0">
                                                    <div className="text-right space-y-0.5">
                                                      <span className="text-[9px] font-extrabold text-clinical-teal-600 dark:text-clinical-teal-400 uppercase block">Likelihood</span>
                                                      <div className="h-1.5 w-24 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden mt-0.5">
                                                        <div 
                                                          className="h-full bg-gradient-to-r from-clinical-teal-500 to-clinical-blue-500 rounded-full"
                                                          style={{ width: `${allergen.score}%` }}
                                                        ></div>
                                                      </div>
                                                      <span className="text-xs font-bold text-slate-700 dark:text-slate-300 block">{allergen.score.toFixed(0)}%</span>
                                                    </div>
                                                    
                                                    <div className="flex-shrink-0">
                                                      {isAlreadyKnown ? (
                                                        <span className="inline-flex items-center gap-1 text-[9px] font-bold bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-550 border border-slate-200 dark:border-slate-705 px-2 py-1 rounded-lg uppercase">
                                                          <Check className="w-3 h-3 text-slate-400" />
                                                          <span>In Profile</span>
                                                        </span>
                                                      ) : (
                                                        <button
                                                          type="button"
                                                          onClick={() => addAllergenToProfile(allergen.id)}
                                                          className="inline-flex items-center gap-1 text-[9px] font-bold bg-clinical-teal-600 hover:bg-clinical-teal-700 text-white px-2 py-1 rounded-lg shadow-xs transition-all uppercase hover:-translate-y-0.5 cursor-pointer"
                                                        >
                                                          <Plus className="w-3 h-3 text-white" />
                                                          <span>Add to Profile</span>
                                                        </button>
                                                      )}
                                                    </div>
                                                  </div>
                                                </div>
                                              );
                                            })}
                                            
                                            {addedAllergenId && (
                                              <div className="bg-clinical-teal-50 dark:bg-clinical-teal-950/20 border border-clinical-teal-200 dark:border-clinical-teal-900/40 text-clinical-teal-800 dark:text-clinical-teal-300 text-[10px] font-bold p-3 rounded-xl flex items-center justify-center gap-2 transition-colors duration-500">
                                                <CheckCircle className="w-4 h-4 text-clinical-teal-600" />
                                                <span>Allergen "{allergens.find(a => a.id === addedAllergenId)?.name}" successfully added to your profile!</span>
                                              </div>
                                            )}
                                          </div>
                                        ) : (
                                          <div className="text-center py-8 space-y-2">
                                            <Info className="w-6 h-6 text-slate-400 dark:text-slate-500 mx-auto" />
                                            <p className="font-bold text-slate-700 dark:text-slate-300 text-xs">No primary allergen matched the profile.</p>
                                          </div>
                                        )}
                                      </div>
                                    )}
 
                                    {idx === 2 && (
                                      <div className="space-y-4 font-medium text-xs text-slate-600 dark:text-slate-350 leading-relaxed font-semibold">
                                        <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
                                          <span>Clinical Mechanism & Next Steps</span>
                                          <span className="text-[9px] bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 font-bold py-0.5 px-2 rounded uppercase">Educational Reference</span>
                                        </h3>
                                        <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-4 rounded-xl space-y-2 shadow-xs transition-colors duration-500">
                                          <span className="text-[10px] font-black uppercase text-clinical-teal-700 dark:text-clinical-teal-400 tracking-wider">Biological Mechanism:</span>
                                          <p className="mt-1 font-semibold text-slate-700 dark:text-slate-300">{unknownAssessment.doctor_note.mechanism}</p>
                                        </div>
                                        <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-4 rounded-xl space-y-2 shadow-xs transition-colors duration-500">
                                          <span className="text-[10px] font-black uppercase text-rose-700 dark:text-rose-400 tracking-wider">When to seek an Allergist:</span>
                                          <ul className="list-disc list-inside space-y-1.5 font-semibold text-slate-700 dark:text-slate-300">
                                            {unknownAssessment.doctor_note.see_doctor_bullets.map((bullet, i) => (
                                              <li key={i}>{bullet}</li>
                                            ))}
                                          </ul>
                                        </div>
                                        <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-4 rounded-xl space-y-2 shadow-xs transition-colors duration-500">
                                          <span className="text-[10px] font-black uppercase text-indigo-700 dark:text-indigo-400 tracking-wider">Expected Allergist visit:</span>
                                          <p className="mt-1 font-semibold text-slate-700 dark:text-slate-300">{unknownAssessment.doctor_note.allergist_evaluation}</p>
                                        </div>
                                        <div className="p-3 bg-rose-50 dark:bg-rose-950/20 border border-rose-100 dark:border-rose-900/40 text-rose-800 dark:text-rose-350 text-[10px] rounded-lg font-bold">
                                          ⚠️ {unknownAssessment.doctor_note.disclaimer}
                                        </div>
                                      </div>
                                    )}
 
                                    {idx === 3 && (
                                      <div className="space-y-4">
                                        <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800">Avoidance & Safe Alternatives</h3>
                                        {unknownAssessment.food_guidance.avoid && unknownAssessment.food_guidance.avoid.length > 0 ? (
                                          <div className="grid sm:grid-cols-2 gap-4">
                                            {unknownAssessment.food_guidance.avoid.map(food => (
                                              <div key={food.id} className="bg-white dark:bg-slate-900 border border-rose-100 dark:border-rose-955 rounded-xl overflow-hidden shadow-xs flex flex-col justify-between transition-colors duration-500">
                                                <div className="h-24 bg-slate-50 dark:bg-slate-950 relative">
                                                  <img 
                                                    src={getImageUrl(food.image_path)} 
                                                    alt={food.name}
                                                    className="w-full h-full object-cover"
                                                  />
                                                </div>
                                                <div className="p-3 space-y-1">
                                                  <span className="text-xs font-bold text-slate-800 dark:text-white block">{food.name}</span>
                                                  <span className="text-[9px] text-slate-400 dark:text-slate-500 block font-semibold uppercase">Triggers: {food.triggered_allergens.join(", ")}</span>
                                                </div>
                                                <div className="bg-rose-50/50 dark:bg-rose-950/20 border-t border-rose-50 dark:border-rose-900/20 p-2 text-center">
                                                  <span className="text-[9px] text-rose-800 dark:text-rose-300 font-bold block">Safe Alternative:</span>
                                                  <span className="text-xs text-rose-700 dark:text-rose-405 font-bold">{food.alternatives[0]}</span>
                                                </div>
                                              </div>
                                            ))}
                                          </div>
                                        ) : (
                                          <div className="text-center py-8 text-slate-400 dark:text-slate-500 text-xs italic font-semibold">
                                            No specific seeded dishes matched the identified allergen profile. Follow general ingredient avoidances.
                                          </div>
                                        )}
 
                                        {unknownAssessment.food_guidance.alternatives && unknownAssessment.food_guidance.alternatives.length > 0 && (
                                          <div className="space-y-2 pt-3 border-t border-slate-100 dark:border-slate-800">
                                            <h4 className="text-[10px] font-bold uppercase tracking-wider text-clinical-teal-700 dark:text-clinical-teal-400">Recommended Safe Alternatives:</h4>
                                            <div className="flex flex-wrap gap-1.5">
                                              {unknownAssessment.food_guidance.alternatives.map((alt, i) => (
                                                <span key={i} className="bg-clinical-teal-50 dark:bg-clinical-teal-950/20 border border-clinical-teal-100 dark:border-clinical-teal-900/40 text-clinical-teal-800 dark:text-clinical-teal-300 text-[10px] px-2.5 py-1 rounded-full font-bold shadow-xs">
                                                  {alt.name} (for {alt.for_food})
                                                </span>
                                              ))}
                                            </div>
                                          </div>
                                        )}
                                      </div>
                                    )}
 
                                    {idx === 4 && (
                                      <div className="space-y-4 text-xs font-semibold">
                                        <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
                                          <span>Stage-based Medical Pathways</span>
                                          <span className="text-[9px] bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 font-bold py-0.5 px-2 rounded uppercase">No Brand names</span>
                                        </h3>
                                        <div className="bg-rose-600/10 dark:bg-rose-950/20 border border-rose-600/20 dark:border-rose-900/40 text-rose-800 dark:text-rose-300 rounded-xl p-3 text-[10px] font-bold">
                                          🚨 {unknownAssessment.medicine_guidance.disclaimer}
                                        </div>
                                        <div className="grid md:grid-cols-2 gap-5">
                                          <div className="space-y-3">
                                            <span className="text-[10px] font-black uppercase text-clinical-blue-700 dark:text-clinical-blue-400 tracking-wider block">Stage A: Pre-Diagnosis OTC Classes</span>
                                            {unknownAssessment.medicine_guidance.stage_a && unknownAssessment.medicine_guidance.stage_a.length > 0 ? (
                                              <div className="space-y-2">
                                                {unknownAssessment.medicine_guidance.stage_a.map((med, i) => (
                                                  <div key={i} className="flex gap-2.5 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-2.5 rounded-xl shadow-xs transition-colors duration-500">
                                                    {med.image_path && (
                                                      <img 
                                                        src={getImageUrl(med.image_path)} 
                                                        alt={med.category} 
                                                        className="w-11 h-11 rounded-lg object-cover bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex-shrink-0"
                                                      />
                                                    )}
                                                    <div className="space-y-0.5 flex-grow">
                                                      <span className="text-xs font-bold text-slate-700 dark:text-white block">{med.category}</span>
                                                      <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-normal font-medium">{med.description}</p>
                                                      <span className="text-[8px] text-amber-700 dark:text-amber-400 font-bold block mt-0.5">Warning: {med.warning}</span>
                                                    </div>
                                                  </div>
                                                ))}
                                              </div>
                                            ) : (
                                              <p className="text-xs text-slate-400 dark:text-slate-505 italic font-semibold">No specific Stage A medicines mapped.</p>
                                            )}
                                          </div>
                                          
                                          <div className="space-y-3">
                                            <span className="text-[10px] font-black uppercase text-indigo-700 dark:text-indigo-400 tracking-wider block">Stage B: Post-Diagnosis Protocols</span>
                                            {unknownAssessment.medicine_guidance.stage_b && unknownAssessment.medicine_guidance.stage_b.length > 0 ? (
                                              <div className="space-y-2">
                                                {unknownAssessment.medicine_guidance.stage_b.map((med, i) => (
                                                  <div key={i} className="flex gap-2.5 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 p-2.5 rounded-xl shadow-xs transition-colors duration-500">
                                                    {med.image_path && (
                                                      <img 
                                                        src={getImageUrl(med.image_path)} 
                                                        alt={med.category} 
                                                        className="w-11 h-11 rounded-lg object-cover bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 flex-shrink-0"
                                                      />
                                                    )}
                                                    <div className="space-y-0.5 flex-grow">
                                                      <span className="text-xs font-bold text-slate-700 dark:text-white block">{med.category}</span>
                                                      <p className="text-[10px] text-slate-500 dark:text-slate-400 leading-normal font-medium">{med.description}</p>
                                                      <span className="text-[8px] text-rose-700 dark:text-rose-450 font-bold block mt-0.5">Warning: {med.warning}</span>
                                                    </div>
                                                  </div>
                                                ))}
                                              </div>
                                            ) : (
                                              <p className="text-xs text-slate-400 dark:text-slate-505 italic font-semibold">No specific Stage B medicines mapped.</p>
                                            )}
                                          </div>
                                        </div>
                                      </div>
                                    )}
 
                                    {idx === 5 && (
                                      <div className="space-y-4">
                                        <h3 className="text-sm font-black text-slate-800 dark:text-white pb-2 border-b border-slate-100 dark:border-slate-800">Electronic Health Record</h3>
                                        
                                        {/* EHR Mini Block */}
                                        <div className="border border-slate-300 dark:border-slate-700 p-4 rounded-xl bg-white dark:bg-slate-900 space-y-3 shadow-xs text-xs transition-colors duration-500">
                                          <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
                                            <div className="flex items-center gap-2">
                                              <Activity className="w-4 h-4 text-slate-900 dark:text-white" />
                                              <h4 className="font-bold text-slate-900 dark:text-white uppercase">ALLERGYGUARD RISK ASSESSMENT</h4>
                                            </div>
                                            <div className="text-right text-[10px] font-semibold text-slate-500 dark:text-slate-400 space-y-0.5">
                                              <div>ID: {reportId}</div>
                                              <div>Account: {userEmail || "GUEST"}</div>
                                              {patientName && <div>Name: <span className="font-bold text-slate-800 dark:text-slate-200">{patientName}</span></div>}
                                              {(patientAge || patientGender) && (
                                                <div>
                                                  {patientAge && `Age: ${patientAge}`}
                                                  {patientAge && patientGender && " | "}
                                                  {patientGender && `Gender: ${patientGender}`}
                                                </div>
                                              )}
                                            </div>
                                          </div>
                                          <div className="space-y-1">
                                            <span className="text-slate-400 dark:text-slate-550 font-bold block uppercase text-[9px]">Likely Allergen Triggers:</span>
                                            <span className="font-bold text-slate-800 dark:text-rose-400 text-xs text-rose-700">
                                              {unknownAssessment.top_allergens?.map(a => `${a.name} (${a.score.toFixed(0)}%)`).join(", ") || "None Identified"}
                                            </span>
                                          </div>
                                          <div className="space-y-1">
                                            <span className="text-slate-400 dark:text-slate-550 font-bold block uppercase text-[9px]">Dietary Warnings:</span>
                                            <span className="font-medium text-slate-700 dark:text-slate-350">
                                              Avoid dishes containing: {unknownAssessment.top_allergens?.map(a => a.name).join(", ") || "No triggers detected"}
                                            </span>
                                          </div>
                                        </div>
                                        
                                        <button
                                          type="button"
                                          onClick={() => window.print()}
                                          className="w-full flex items-center justify-center gap-1.5 text-xs font-bold bg-slate-900 dark:bg-slate-800 hover:bg-black dark:hover:bg-slate-750 text-white py-2.5 rounded-xl shadow-xs transition-colors cursor-pointer"
                                        >
                                          <Printer className="w-4 h-4" />
                                          <span>Print/Save EHR PDF Report</span>
                                        </button>
                                      </div>
                                    )}
 
                                    {/* Step Inner Navigation Controls */}
                                    <div className="mt-5 flex items-center justify-between pt-4 border-t border-slate-100/80 dark:border-slate-800">
                                      <button
                                        type="button"
                                        disabled={idx === 0}
                                        onClick={(e) => { e.stopPropagation(); setActiveStep(idx - 1); }}
                                        className={`text-[10px] font-bold px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-705 transition-colors ${
                                          idx === 0 
                                            ? "text-slate-300 dark:text-slate-600 bg-slate-50/50 dark:bg-slate-850/50 cursor-not-allowed border-slate-100 dark:border-slate-800" 
                                            : "text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800"
                                        }`}
                                      >
                                        Back
                                      </button>
                                      
                                      {idx < 5 ? (
                                        <button
                                          type="button"
                                          onClick={(e) => { e.stopPropagation(); setActiveStep(idx + 1); }}
                                          className="text-[10px] font-bold bg-clinical-blue-600 hover:bg-clinical-blue-700 text-white px-4 py-1.5 rounded-xl shadow-sm transition-all hover:-translate-y-0.5 cursor-pointer"
                                        >
                                          Next Step
                                        </button>
                                      ) : (
                                        <button
                                          type="button"
                                          onClick={(e) => {
                                            e.stopPropagation();
                                            resetUnknownForm();
                                          }}
                                          className="text-[10px] font-bold bg-slate-900 dark:bg-slate-800 hover:bg-black dark:hover:bg-slate-750 text-white px-4 py-1.5 rounded-xl shadow-sm transition-all hover:-translate-y-0.5 cursor-pointer"
                                        >
                                          Reset Assessment
                                        </button>
                                      )}
                                    </div>

                                  </div>
                                </motion.div>
                              )}
                            </AnimatePresence>
                          </div>
                        );
                      })}
                    </div>

                    {/* Hidden Printable Report Card (Independent from screen accordion state) */}
                    <div className="hidden print:block print-report">
                      <div className="border-4 border-double border-slate-800 p-5 rounded-2xl bg-white space-y-4">
                        <div className="flex flex-col sm:flex-row items-start justify-between gap-4 pb-4 border-b-2 border-slate-800">
                          <div className="space-y-1">
                            <div className="flex items-center gap-2">
                              <div className="w-8 h-8 rounded bg-slate-900 flex items-center justify-center text-white print:border print:border-black">
                                <Activity className="w-5 h-5" />
                              </div>
                              <h2 className="text-xl font-black text-slate-900 tracking-tight uppercase">ALLERGYGUARD RISK REPORT</h2>
                            </div>
                            <p className="text-xs text-slate-500 font-bold tracking-wide">ELECTRONIC HEALTH RECORD ASSESSMENT FILE</p>
                          </div>
                          
                          <div className="text-left sm:text-right text-xs font-semibold text-slate-700 space-y-1">
                            <div><span className="text-slate-400">Report ID:</span> <span className="font-bold text-slate-800">{reportId}</span></div>
                            <div><span className="text-slate-400">Date/Time:</span> <span className="font-bold text-slate-800">{reportDate}</span></div>
                            <div><span className="text-slate-400">Account:</span> <span className="font-bold text-slate-800">{userEmail || "MOCK-GUEST"}</span></div>
                          </div>
                        </div>

                        {/* Section 0: Patient Demographics */}
                        {(patientName || patientAge || patientGender) && (
                          <div className="space-y-2 no-break-print pb-3 border-b border-slate-200 text-xs">
                            <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider">Patient Demographics</h4>
                            <div className="grid grid-cols-3 gap-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100 font-semibold">
                              <div>
                                <span className="text-slate-400 block font-bold text-[10px] uppercase">Name</span>
                                <span className="text-slate-800 font-bold">{patientName || "Not Specified"}</span>
                              </div>
                              <div>
                                <span className="text-slate-400 block font-bold text-[10px] uppercase">Age</span>
                                <span className="text-slate-800 font-bold">{patientAge ? `${patientAge} yrs` : "Not Specified"}</span>
                              </div>
                              <div>
                                <span className="text-slate-400 block font-bold text-[10px] uppercase">Gender</span>
                                <span className="text-slate-800 font-bold">{patientGender || "Not Specified"}</span>
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Section 1: Presentation */}
                        <div className="space-y-2 no-break-print pb-3 border-b border-slate-200">
                          <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider">I. Patient Clinical Presentation</h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                            <div>
                              <span className="text-slate-400 block font-bold">Food Consumed:</span>
                              <span className="font-bold text-slate-800 uppercase">
                                {selectedFoodId ? selectedFoodId.replace("_", " ") : (unknownAssessment.extracted_foods?.[0]?.replace("_", " ") || "Not Specified")}
                              </span>
                            </div>
                            <div>
                              <span className="text-slate-400 block font-bold">Selected Symptoms:</span>
                              <span className="font-semibold text-slate-800 leading-normal">
                                {selectedSymptoms.map(sId => symptoms.find(s => s.id === sId)?.name || sId).join(", ") || "None"}
                              </span>
                            </div>
                            {unknownAssessment.photo_analysis && (
                              <div className="md:col-span-2">
                                <span className="text-slate-400 block font-bold">Visual Pattern analysis:</span>
                                <span className="font-bold text-clinical-teal-700 uppercase">
                                  {unknownAssessment.photo_analysis.label} ({(unknownAssessment.photo_analysis.confidence * 100).toFixed(0)}% confidence match)
                                </span>
                              </div>
                            )}
                          </div>
                        </div>

                        {/* Section 2: Likely Allergens */}
                        <div className="space-y-2 no-break-print pb-3 border-b border-slate-200">
                          <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider">II. Top Matched Allergen Profiles</h4>
                          {unknownAssessment.top_allergens && unknownAssessment.top_allergens.length > 0 ? (
                            <table className="w-full text-left text-xs border-collapse">
                              <thead>
                                <tr className="border-b border-slate-300">
                                  <th className="py-2 font-black text-slate-700">Allergen Trigger</th>
                                  <th className="py-2 font-black text-slate-700">Clinical Description</th>
                                  <th className="py-2 font-black text-slate-700 text-right">Confidence Match</th>
                                </tr>
                              </thead>
                              <tbody>
                                {unknownAssessment.top_allergens.map(a => (
                                  <tr key={a.id} className="border-b border-slate-100">
                                    <td className="py-2 font-extrabold text-slate-800">{a.name}</td>
                                    <td className="py-2 text-slate-500 pr-4">{a.description}</td>
                                    <td className="py-2 font-black text-slate-800 text-right">{a.score.toFixed(0)}%</td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          ) : (
                            <p className="text-xs italic text-slate-400">No matched allergens identified.</p>
                          )}
                        </div>

                        {/* Section 3: Food & Medicine Guidances */}
                        <div className="space-y-3 no-break-print pb-3 border-b border-slate-200">
                          <h4 className="text-xs font-black uppercase text-slate-800 tracking-wider">III. Patient Management & Guidance Summary</h4>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs leading-normal font-medium">
                            <div className="space-y-1">
                              <span className="text-slate-400 block font-bold">Food Avoidances:</span>
                              <p className="text-slate-600">
                                Avoid eating dishes containing: <span className="font-bold text-rose-700">{unknownAssessment.top_allergens?.map(a => a.name).join(", ") || "identified allergens"}</span>.
                              </p>
                              {unknownAssessment.food_guidance.avoid && unknownAssessment.food_guidance.avoid.length > 0 && (
                                <p className="text-[11px] text-slate-500 font-bold uppercase mt-1">
                                  Specific dishes to avoid: {unknownAssessment.food_guidance.avoid.map(x => x.name).join(", ")}
                                </p>
                              )}
                            </div>
                            <div className="space-y-1">
                              <span className="text-slate-400 block font-bold">Medicine Category Recommendations:</span>
                              <p className="text-slate-600">
                                OTC Relief (Stage A): {unknownAssessment.medicine_guidance.stage_a?.map(m => m.category).join(", ") || "Antihistamines"}.
                              </p>
                              <p className="text-slate-600">
                                Clinical Prescriptions (Stage B): {unknownAssessment.medicine_guidance.stage_b?.map(m => m.category).join(", ") || "Epinephrine"}.
                              </p>
                            </div>
                          </div>
                        </div>

                        {/* Section 4: Academic Warning */}
                        <div className="pt-2 no-break-print flex flex-col items-center text-center space-y-1.5">
                          <span className="text-[10px] text-amber-800 bg-amber-500/10 font-black px-4 py-1.5 rounded-full border border-amber-500/20 uppercase tracking-wide leading-none">
                            ⚠️ ACADEMIC REFERENCE STUDY FILE — NOT FOR DIAGNOSTIC USE
                          </span>
                          <p className="text-[10px] text-slate-400 font-medium max-w-lg">
                            This file is a programmatically generated assessment stub created for educational demonstration. It is not signed by a certified board allergist. Confirm all clinical decisions with a physician.
                          </p>
                        </div>
                      </div>
                    </div>

                  </div>
                )}
              </motion.div>
            )}

            {/* --- TAB: PROFILE --- */}
            {activeTab === "profile" && (
              <motion.div 
                key="profile"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                className="max-w-4xl mx-auto space-y-8 print:hidden"
              >
                <div className="border-b border-slate-100 dark:border-slate-800 pb-5">
                  <h2 className="text-2xl md:text-3xl font-semibold text-slate-900 dark:text-white transition-colors duration-500">Patient Dashboard</h2>
                  <p className="text-base text-slate-500 dark:text-slate-400 leading-relaxed font-normal mt-1 transition-colors duration-500">Access your personalized profiles, save known allergies, and view saved clinical risk assessments.</p>
                </div>

                {!userToken ? (
                  /* Login/Register Panel */
                  <div className="max-w-md mx-auto bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-3xl p-6 sm:p-8 shadow-xl space-y-6 transition-colors duration-500">
                    <div className="text-center space-y-2">
                      <div className="w-12 h-12 rounded-full bg-clinical-teal-50 dark:bg-clinical-teal-950/40 flex items-center justify-center text-clinical-teal-600 dark:text-clinical-teal-400 mx-auto">
                        <User className="w-6 h-6" />
                      </div>
                      <h3 className="text-xl font-bold text-slate-800 dark:text-white">{authMode === "login" ? "Sign In to AllergyGuard" : "Create Patient Account"}</h3>
                      <p className="text-xs text-slate-400 dark:text-slate-500">Save your known triggers and track your exposure logs over time.</p>
                    </div>

                    <form onSubmit={handleAuth} className="space-y-4">
                      {authError && (
                        <div className="bg-rose-50 dark:bg-rose-950/20 border border-rose-100 dark:border-rose-900/40 text-rose-700 dark:text-rose-300 text-xs font-bold p-3 rounded-lg flex items-center gap-1.5">
                          <XCircle className="w-4 h-4 text-rose-600 flex-shrink-0" />
                          <span>{authError}</span>
                        </div>
                      )}

                      {authMode === "register" && (
                        <div className="space-y-1.5">
                          <label className="text-xs font-bold text-slate-500 dark:text-slate-400 block">Full Name</label>
                          <input 
                            type="text"
                            required
                            value={authName}
                            onChange={e => setAuthName(e.target.value)}
                            placeholder="John Doe"
                            className="w-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-clinical-teal-500 transition-colors duration-500"
                          />
                        </div>
                      )}

                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-500 dark:text-slate-400 block">Email Address</label>
                        <input 
                          type="email"
                          required
                          value={authEmail}
                          onChange={e => setAuthEmail(e.target.value)}
                          placeholder="patient@allergyguard.org"
                          className="w-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-clinical-teal-500 transition-colors duration-500"
                        />
                      </div>

                      <div className="space-y-1.5">
                        <label className="text-xs font-bold text-slate-500 dark:text-slate-400 block">Password</label>
                        <input 
                          type="password"
                          required
                          value={authPassword}
                          onChange={e => setAuthPassword(e.target.value)}
                          placeholder="••••••••"
                          className="w-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-800 dark:text-slate-100 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-clinical-teal-500 transition-colors duration-500"
                        />
                      </div>

                      <button 
                        type="submit"
                        className="w-full bg-gradient-to-r from-clinical-teal-600 to-clinical-blue-600 hover:from-clinical-teal-700 hover:to-clinical-blue-700 text-white font-bold text-sm py-3 px-6 rounded-xl shadow-md transition-all mt-2 cursor-pointer"
                      >
                        {authMode === "login" ? "Sign In" : "Register"}
                      </button>
                    </form>

                    <div className="text-center border-t border-slate-100 dark:border-slate-800 pt-4">
                      <button 
                        onClick={() => setAuthMode(authMode === "login" ? "register" : "login")}
                        className="text-xs text-clinical-teal-600 dark:text-clinical-teal-400 font-bold hover:underline cursor-pointer"
                      >
                        {authMode === "login" ? "Don't have an account? Register" : "Already have an account? Sign In"}
                      </button>
                    </div>
                  </div>
                ) : (
                  /* Profile Details & Logs */
                  <div className="grid md:grid-cols-12 gap-8">
                    
                    {/* User Card */}
                    <div className="md:col-span-4 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-4 self-start transition-colors duration-500">
                      <div className="text-center space-y-1">
                        <div className="w-16 h-16 rounded-full bg-clinical-teal-50 dark:bg-clinical-teal-950/40 text-clinical-teal-600 dark:text-clinical-teal-455 flex items-center justify-center mx-auto border-2 border-clinical-teal-100 dark:border-clinical-teal-900 font-bold text-lg uppercase transition-all duration-500">
                          {userName ? userName.substring(0, 2) : (userEmail ? userEmail.substring(0, 2) : "PT")}
                        </div>
                        <h4 className="font-bold text-slate-800 dark:text-white line-clamp-1 transition-colors duration-500">{userName || userEmail || "Patient Profile"}</h4>
                        {userName && <p className="text-xs text-slate-400 dark:text-slate-500 line-clamp-1 transition-colors duration-500">{userEmail}</p>}
                        <span className="text-[10px] bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 font-bold px-2 py-0.5 rounded-full uppercase tracking-wider inline-block mt-1 transition-colors duration-500">Patient Status</span>
                      </div>
                      
                      <div className="border-t border-slate-100 dark:border-slate-800 pt-4 text-center">
                        <button 
                          onClick={handleLogout}
                          className="w-full border border-slate-200 dark:border-slate-700 hover:bg-rose-50 dark:hover:bg-rose-950/30 text-slate-600 dark:text-slate-300 hover:text-rose-600 dark:hover:text-rose-455 text-xs font-bold py-2.5 px-4 rounded-xl transition-all flex items-center justify-center gap-1.5 cursor-pointer"
                        >
                          <LogOut className="w-4 h-4" />
                          <span>Logout Session</span>
                        </button>
                      </div>
                    </div>

                    {/* Historical Logs List */}
                    <div className="md:col-span-8 bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-5 shadow-sm space-y-5 transition-colors duration-500">
                      <h3 className="text-base font-bold text-slate-800 dark:text-white pb-3 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
                        <span>Risk Assessment History</span>
                        <span className="text-xs bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 font-bold py-0.5 px-2 rounded-full">{historyLogs.length} Records</span>
                      </h3>

                      {isLoadingHistory ? (
                        <div className="h-32 flex items-center justify-center">
                          <RefreshCw className="w-5 h-5 text-clinical-teal-500 animate-spin" />
                        </div>
                      ) : historyLogs.length === 0 ? (
                        <div className="text-center py-12 text-slate-400 dark:text-slate-500 text-xs italic font-medium">
                          No allergy logs saved yet. Submit a Risk Assessment form to start history logging.
                        </div>
                      ) : (
                        <div className="space-y-4">
                          {historyLogs.map(log => (
                            <div key={log.id} className="border border-slate-100 dark:border-slate-800 rounded-xl p-4 bg-slate-50/50 dark:bg-slate-950/30 space-y-3 transition-colors duration-500">
                              <div className="flex items-center justify-between gap-4">
                                <span className="text-[10px] text-slate-400 dark:text-slate-500 font-bold block">{new Date(log.created_at).toLocaleString()}</span>
                                {log.results.severe_symptom_detected && (
                                  <span className="text-[9px] bg-rose-600 text-white font-extrabold px-1.5 py-0.5 rounded uppercase tracking-wider pulse-emergency-banner">Severe</span>
                                )}
                              </div>
                              
                              <p className="text-xs text-slate-600 dark:text-slate-350 font-semibold line-clamp-2">{log.query_text}</p>
                              
                              {/* Top allergens summary */}
                              {log.results.top_allergens && log.results.top_allergens.length > 0 && (
                                <div className="flex flex-wrap gap-1 pt-1 items-center">
                                  <span className="text-[9px] text-slate-400 dark:text-slate-550 font-bold block mr-1 uppercase">Top Triggers:</span>
                                  {log.results.top_allergens.map(a => (
                                    <span key={a.id} className="text-[10px] font-bold bg-clinical-teal-50 dark:bg-clinical-teal-950/20 border border-clinical-teal-100 dark:border-clinical-teal-900/40 text-clinical-teal-800 dark:text-clinical-teal-300 px-2 py-0.5 rounded">
                                      {a.name} ({a.score.toFixed(0)}%)
                                    </span>
                                  ))}
                                </div>
                              )}
                              
                              {log.photo_url && (
                                <div className="flex items-center gap-2 pt-1">
                                  <ImageIcon className="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
                                  <span className="text-[10px] text-slate-400 dark:text-slate-550 font-bold">Photo analyzed: {log.photo_analysis?.label}</span>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      )}
                    </div>

                  </div>
                )}
              </motion.div>
            )}

            {/* --- TAB: ABOUT & TECHNICAL DETAILS --- */}
            {activeTab === "about" && (
              <motion.div 
                key="about"
                initial={{ opacity: 0, y: 15 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -15 }}
                className="max-w-4xl mx-auto space-y-8 print:hidden"
              >
                <div className="border-b border-slate-100 dark:border-slate-800 pb-5">
                  <h2 className="text-2xl md:text-3xl font-semibold text-slate-900 dark:text-white transition-colors duration-500">Academic Project Specifications</h2>
                  <p className="text-base text-slate-500 dark:text-slate-400 leading-relaxed font-normal mt-1 transition-colors duration-500">AllergyGuard is a full-stack student demo combining natural language entity parsing and image color distribution matching.</p>
                </div>

                <div className="bg-white dark:bg-slate-900 border border-slate-100 dark:border-slate-800 rounded-2xl p-6 shadow-sm space-y-6 text-sm text-slate-600 dark:text-slate-350 font-medium leading-relaxed transition-colors duration-500">
                  
                  <div>
                    <h3 className="font-bold text-slate-800 dark:text-white text-base">Natural Language Processing (NLP) Engine</h3>
                    <p className="mt-1">
                      Our backend relies on the Python **spaCy** NLP engine. We instantiate a custom `EntityRuler` pipeline loading token-based matcher patterns. When a patient describes their symptoms (e.g. <i>"I ate moong beans and then my throat started tightening. I also feel dizzy..."</i>), the rules identify food triggers and symptoms by handling token lists, negations, and wildcards natively, then mapping them to unique database primary keys.
                    </p>
                  </div>

                  <div className="pt-4 border-t border-slate-100 dark:border-slate-800">
                    <h3 className="font-bold text-slate-800 dark:text-white text-base">Computer Vision Pattern Matching</h3>
                    <p className="mt-1">
                      Reaction photographs uploaded to the Unknown Allergy Module are parsed by our lightweight visual model stub built with Python's **Pillow** library. It evaluates color space coordinates, calculating redness ratios and spatial clustering (using coordinate variance and standard deviations) to distinguish between localized patches (urticaria), uniform skin flushing (diffuse redness), pale skin angioedema (swelling), or noise (inconclusive).
                    </p>
                  </div>

                  <div className="pt-4 border-t border-slate-100 dark:border-slate-800">
                    <h3 className="font-bold text-slate-800 dark:text-white text-base">Supabase Database Integration</h3>
                    <p className="mt-1">
                      The application database layer is isolated in <code>db.py</code>. During development, it is wired to a local JSON database. For production, the database client connects to a **Supabase (PostgreSQL)** backend configured with Row Level Security (RLS), supporting encrypted email/password authentication, query logs JSONB serialization, and public image assets storage buckets.
                    </p>
                  </div>

                  <div className="pt-4 border-t border-slate-100 dark:border-slate-800 bg-amber-500/10 dark:bg-amber-950/20 border-l-4 border-amber-500 rounded-xl p-4 text-xs text-amber-800 dark:text-amber-300 font-bold">
                    ⚠️ ACADEMIC PROJECT LIMITATIONS: This software does not provide real clinical advice. It is a proof-of-concept student prototype. Do not make medical decisions using this dashboard.
                  </div>

                </div>
              </motion.div>
            )}

          </AnimatePresence>
        )}

      </main>

      {/* 5. Main Footer */}
      <footer className="bg-slate-900 dark:bg-slate-950 text-slate-400 dark:text-slate-550 py-16 border-t border-slate-800 dark:border-slate-900 text-xs print:hidden transition-colors duration-500">
        <div className="max-w-7xl mx-auto px-6 md:px-12 space-y-6">
          
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 border-b border-slate-800 pb-6">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-lg bg-clinical-teal-600 flex items-center justify-center">
                <Activity className="w-3.5 h-3.5 text-white" />
              </div>
              <span className="font-bold text-white tracking-tight">AllergyGuard</span>
            </div>
            <p className="text-center sm:text-right font-medium">AllergyGuard Academic health-tech concept project © 2026. All rights reserved.</p>
          </div>

          <div className="space-y-3 leading-relaxed text-slate-500 dark:text-slate-600 max-w-4xl font-medium">
            <p>
              <strong>Clinical Safety Warning & Disclaimer:</strong> AllergyGuard is a student demonstration project developed for academic evaluation. It is not an FDA-approved medical device, diagnostic system, or clinical decision support software. The information, scores, medicines, and alternatives provided on this website are for educational simulation purposes only and do not constitute clinical guidance, recommendations, or official diagnoses.
            </p>
            <p>
              Never ignore professional medical advice or delay seeking care because of something you read on this application. If you are experiencing a severe allergic reaction (such as anaphylaxis, difficulty swallowing, or wheezing), please call emergency services immediately (911 / 108 / 112).
            </p>
          </div>

        </div>
      </footer>

    </div>
  );
}
