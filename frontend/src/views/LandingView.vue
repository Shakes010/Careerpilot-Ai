<template>
  <div class="min-h-screen bg-[#F8FAFC] text-[#0F172A] font-sans antialiased">
    
    <!-- Top Navbar -->
    <header class="bg-white/90 backdrop-blur-md sticky top-0 z-50 border-b border-slate-200/80">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        
        <!-- Logo -->
        <router-link to="/" class="flex items-center gap-2.5 group">
          <div class="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20 group-hover:bg-blue-700 transition-all">
            <svg class="w-5 h-5 -rotate-45 transform translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </div>
          <span class="text-2xl font-extrabold tracking-tight text-[#0F172A]">CareerPilot <span class="text-[#2563EB]">AI</span></span>
        </router-link>

        <!-- Navigation Links -->
        <nav class="hidden md:flex items-center gap-8 text-sm font-semibold text-slate-600">
          <a href="#features" class="hover:text-[#2563EB] transition-colors">Features</a>
          <a href="#students" class="hover:text-[#2563EB] transition-colors">For Students</a>
          <a href="#recruiters" class="hover:text-[#2563EB] transition-colors">For Recruiters</a>
          <div class="relative group cursor-pointer flex items-center gap-1 hover:text-[#2563EB] transition-colors">
            <span>Resources</span>
            <svg class="w-4 h-4 text-slate-400 group-hover:text-[#2563EB]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
          <a href="#about" class="hover:text-[#2563EB] transition-colors">About Us</a>
        </nav>

        <!-- Right CTAs -->
        <div class="flex items-center gap-3">
          <router-link to="/login" class="px-5 py-2.5 text-sm font-bold text-slate-700 hover:text-[#2563EB] bg-white hover:bg-blue-50 border border-slate-300 rounded-xl transition-all">
            Login
          </router-link>
          <router-link to="/login?signup=true" class="px-5 py-2.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-blue-700 rounded-xl shadow-md shadow-blue-500/20 hover:shadow-lg transition-all">
            Get Started Free
          </router-link>
        </div>

      </div>
    </header>

    <!-- Hero Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
      
      <!-- Left Hero Content -->
      <div class="space-y-6">
        
        <!-- Pill Badge -->
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-50 border border-blue-200/80 text-xs font-bold text-[#2563EB]">
          <svg class="w-3.5 h-3.5 text-[#2563EB]" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/>
          </svg>
          <span>AI-Powered Career Development Platform</span>
        </div>

        <!-- Headline -->
        <h1 class="text-4xl md:text-5xl lg:text-6xl font-black text-[#0F172A] tracking-tight leading-[1.12]">
          Your Career.<br />
          Your Journey.<br />
          <span class="text-[#2563EB]">Our Mission.</span>
        </h1>

        <!-- Subtitle -->
        <p class="text-base md:text-lg text-slate-600 leading-relaxed max-w-lg">
          CareerPilot AI helps students build verified skills, create impressive portfolios and connect with opportunities that shape the future.
        </p>

        <!-- Hero Action Buttons -->
        <div class="flex flex-wrap items-center gap-4 pt-2">
          <router-link to="/login?signup=true" class="px-7 py-3.5 text-sm font-bold text-white bg-[#2563EB] hover:bg-blue-700 rounded-xl shadow-lg shadow-blue-500/25 hover:shadow-xl transition-all flex items-center gap-2">
            <span>Get Started For Free</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </router-link>
          
          <a href="#demo" class="px-6 py-3.5 text-sm font-bold text-[#0F172A] bg-white border border-slate-300 hover:bg-slate-50 rounded-xl shadow-xs transition-all flex items-center gap-2.5">
            <div class="w-6 h-6 rounded-full bg-blue-50 text-[#2563EB] flex items-center justify-center">
              <svg class="w-3.5 h-3.5 translate-x-0.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M8 5v14l11-7z"/>
              </svg>
            </div>
            <span>Watch Demo</span>
          </a>
        </div>

        <!-- Social Proof -->
        <div class="pt-6 flex items-center gap-4 border-t border-slate-200">
          <div class="flex -space-x-2">
            <div class="w-9 h-9 rounded-full border-2 border-white bg-blue-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
              AR
            </div>
            <div class="w-9 h-9 rounded-full border-2 border-white bg-emerald-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
              SJ
            </div>
            <div class="w-9 h-9 rounded-full border-2 border-white bg-indigo-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
              MK
            </div>
          </div>
          <div class="text-xs">
            <div class="font-extrabold text-[#0F172A]">10K+ Students trust us</div>
            <div class="text-amber-500 font-bold flex items-center gap-1 mt-0.5">
              ★★★★★ <span class="text-slate-500 font-semibold">4.8/5 (1200+ Reviews)</span>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Hero Illustration Graphic -->
      <div class="relative">
        <div class="bg-gradient-to-br from-blue-50/80 via-white to-indigo-50/60 p-6 md:p-8 rounded-3xl border border-slate-200/80 shadow-2xl space-y-6 relative overflow-hidden">
          
          <!-- Floating Feature Badges -->
          <div class="flex items-center justify-between gap-4">
            <div class="bg-white px-3.5 py-2 rounded-2xl shadow-md border border-slate-200 flex items-center gap-2.5">
              <div class="w-7 h-7 rounded-lg bg-blue-100 text-[#2563EB] flex items-center justify-center text-xs">
                🤖
              </div>
              <div class="text-left">
                <div class="text-[11px] font-bold text-[#0F172A]">AI Guidance</div>
                <div class="text-[9px] text-slate-500">Personalized Insights</div>
              </div>
            </div>

            <div class="bg-white px-3.5 py-2 rounded-2xl shadow-md border border-slate-200 flex items-center gap-2.5">
              <div class="w-7 h-7 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center text-xs">
                🎯
              </div>
              <div class="text-left">
                <div class="text-[11px] font-bold text-[#0F172A]">Opportunity Radar</div>
                <div class="text-[9px] text-slate-500">Top Matches For You</div>
              </div>
            </div>
          </div>

          <!-- Hero Graphic SVG Vector -->
          <div class="py-6 flex items-center justify-center relative">
            <svg class="w-full max-w-md h-auto" viewBox="0 0 500 300" fill="none" xmlns="http://www.w3.org/2000/svg">
              <!-- Network background lines -->
              <path d="M50 150 Q 150 50, 250 150 T 450 150" stroke="#BFDBFE" stroke-width="2" stroke-dasharray="4 4" />
              <path d="M100 220 Q 250 100, 400 220" stroke="#C7D2FE" stroke-width="2" stroke-dasharray="4 4" />

              <!-- Collaborative Desk & People -->
              <rect x="70" y="200" width="360" height="12" rx="6" fill="#3B82F6" />
              
              <!-- Student 1 -->
              <circle cx="130" cy="140" r="22" fill="#FCA5A5" />
              <rect x="110" y="165" width="40" height="40" rx="10" fill="#2563EB" />
              <rect x="100" y="185" width="50" height="15" rx="3" fill="#64748B" />

              <!-- Student 2 -->
              <circle cx="250" cy="130" r="22" fill="#FDE047" />
              <rect x="230" y="155" width="40" height="45" rx="10" fill="#1E293B" />
              <rect x="220" y="185" width="55" height="15" rx="3" fill="#0284C7" />

              <!-- Student 3 -->
              <circle cx="370" cy="140" r="22" fill="#93C5FD" />
              <rect x="350" y="165" width="40" height="40" rx="10" fill="#059669" />
              <rect x="340" y="185" width="50" height="15" rx="3" fill="#475569" />
            </svg>
          </div>

          <!-- Bottom Card Badge -->
          <div class="bg-white p-3.5 rounded-2xl shadow-md border border-slate-200 flex items-center justify-between w-max mx-auto gap-4">
            <div class="flex items-center gap-2">
              <div class="w-6 h-6 rounded-full bg-blue-100 text-[#2563EB] flex items-center justify-center text-xs font-bold">✓</div>
              <span class="text-xs font-bold text-[#0F172A]">Verified Skills: Showcase your real abilities</span>
            </div>
          </div>

        </div>
      </div>

    </section>

    <!-- Company Logos Banner -->
    <section class="bg-white py-10 border-y border-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center space-y-6">
        <p class="text-xs font-bold text-slate-500 uppercase tracking-wider">Trusted by Students & Leading Companies</p>
        <div class="flex flex-wrap items-center justify-center gap-8 md:gap-16 opacity-70 font-black text-xl text-slate-700 tracking-tight">
          <span class="flex items-center gap-1.5"><span class="w-6 h-6 rounded-lg bg-slate-900 text-white flex items-center justify-center text-xs">tcs</span> tcs</span>
          <span class="flex items-center gap-1.5"><span class="w-6 h-6 rounded-full border-2 border-slate-800 flex items-center justify-center text-xs">i</span> Infosys</span>
          <span class="flex items-center gap-1.5"><span class="w-6 h-6 rounded-full border-2 border-slate-800 flex items-center justify-center text-xs">w</span> wipr<span class="text-blue-600">o</span></span>
          <span class="flex items-center gap-1.5"><span class="w-6 h-6 rounded-full border-2 border-slate-800 flex items-center justify-center text-xs">></span> accenture</span>
          <span class="flex items-center gap-1.5">Deloitte.</span>
          <span class="flex items-center gap-1.5"><span class="w-6 h-6 rounded-full border-2 border-slate-800 flex items-center justify-center text-xs">C</span> Capgemini</span>
        </div>
      </div>
    </section>

    <!-- 6 Feature Cards Grid Section -->
    <section id="features" class="py-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-12">
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        
        <!-- Card 1 -->
        <div class="p-8 rounded-3xl bg-white border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center text-xl font-bold border border-blue-100">
            🤖
          </div>
          <h3 class="text-xl font-bold text-[#0F172A]">AI Guidance</h3>
          <p class="text-sm text-slate-600 leading-relaxed">
            Personalized career recommendations at every step of your development journey.
          </p>
        </div>

        <!-- Card 2 -->
        <div class="p-8 rounded-3xl bg-white border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-blue-50 text-[#2563EB] flex items-center justify-center text-xl font-bold border border-blue-100">
            🛡️
          </div>
          <h3 class="text-xl font-bold text-[#0F172A]">Verified Skills</h3>
          <p class="text-sm text-slate-600 leading-relaxed">
            Get skills verified through real-world projects, assessments, and peer reviews.
          </p>
        </div>

        <!-- Card 3 -->
        <div class="p-8 rounded-3xl bg-white border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center text-xl font-bold border border-amber-100">
            📄
          </div>
          <h3 class="text-xl font-bold text-[#0F172A]">Career Passport</h3>
          <p class="text-sm text-slate-600 leading-relaxed">
            Showcase your journey with a verified profile that stands out to recruiters.
          </p>
        </div>

        <!-- Card 4 -->
        <div class="p-8 rounded-3xl bg-white border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-xl font-bold border border-emerald-100">
            💼
          </div>
          <h3 class="text-xl font-bold text-[#0F172A]">Opportunities</h3>
          <p class="text-sm text-slate-600 leading-relaxed">
            Discover jobs, internships and hackathons catered precisely to your skill tier.
          </p>
        </div>

        <!-- Card 5 -->
        <div class="p-8 rounded-3xl bg-white border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-xl font-bold border border-indigo-100">
            📁
          </div>
          <h3 class="text-xl font-bold text-[#0F172A]">Portfolio Builder</h3>
          <p class="text-sm text-slate-600 leading-relaxed">
            Build stunning, dynamic project portfolios that prove your execution capabilities.
          </p>
        </div>

        <!-- Card 6 -->
        <div class="p-8 rounded-3xl bg-white border border-slate-200 shadow-sm hover:shadow-xl hover:border-blue-300 transition-all space-y-4">
          <div class="w-12 h-12 rounded-2xl bg-pink-50 text-pink-600 flex items-center justify-center text-xl font-bold border border-pink-100">
            🎯
          </div>
          <h3 class="text-xl font-bold text-[#0F172A]">Smart Matching</h3>
          <p class="text-sm text-slate-600 leading-relaxed">
            AI matches you with high-growth roles that perfectly fit your experience.
          </p>
        </div>

      </div>

    </section>

    <!-- Bottom Stats Bar -->
    <section class="bg-white border-t border-slate-200 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid grid-cols-2 md:grid-cols-5 gap-6 text-center">
        
        <div class="space-y-1">
          <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto font-bold text-lg">🎓</div>
          <div class="text-2xl font-black text-[#0F172A]">10K+</div>
          <div class="text-xs text-slate-500 font-semibold">Students Empowered</div>
        </div>

        <div class="space-y-1">
          <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto font-bold text-lg">🎖️</div>
          <div class="text-2xl font-black text-[#0F172A]">500+</div>
          <div class="text-xs text-slate-500 font-semibold">Verified Skills</div>
        </div>

        <div class="space-y-1">
          <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto font-bold text-lg">🏢</div>
          <div class="text-2xl font-black text-[#0F172A]">2K+</div>
          <div class="text-xs text-slate-500 font-semibold">Partner Companies</div>
        </div>

        <div class="space-y-1">
          <div class="w-10 h-10 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center mx-auto font-bold text-lg">💼</div>
          <div class="text-2xl font-black text-[#0F172A]">15K+</div>
          <div class="text-xs text-slate-500 font-semibold">Opportunities Available</div>
        </div>

        <div class="space-y-1 col-span-2 md:col-span-1">
          <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-500 flex items-center justify-center mx-auto font-bold text-lg">🏆</div>
          <div class="text-2xl font-black text-[#0F172A]">95%</div>
          <div class="text-xs text-slate-500 font-semibold">Better Career Outcomes</div>
        </div>

      </div>
    </section>

  </div>
</template>

<script setup>
</script>
