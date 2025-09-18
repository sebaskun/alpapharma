<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-white">
    <!-- Header -->
    <header class="text-center py-12 px-4">
      <div class="max-w-4xl mx-auto">
        <div class="flex items-center justify-center gap-4 mb-6">
          <div class="w-16 h-16 bg-orange-200 rounded-full flex items-center justify-center">
            <span class="text-2xl">🦙</span>
          </div>
          <h1 class="text-4xl font-bold text-gray-900">AlpaPharma</h1>
        </div>
        <p class="text-xl text-gray-600 max-w-2xl mx-auto">
          Upload a pharmaceutical specialist's CV and discover all medical entities - drugs, ingredients, and compounds - with AI-powered analysis.
        </p>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-4xl mx-auto px-4 pb-12">
      <!-- Upload Section -->
      <div v-if="!isAnalyzing && !results" class="bg-white rounded-2xl shadow-lg p-8 border border-orange-100">
        <div class="text-center">
          <div class="border-2 border-dashed border-orange-300 rounded-xl p-12 mb-6 transition-colors hover:border-orange-400">
            <input
              ref="fileInput"
              type="file"
              accept=".pdf"
              @change="handleFileSelect"
              class="hidden"
            >
            <div class="cursor-pointer" @click="$refs.fileInput.click()">
              <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg class="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                </svg>
              </div>
              <p class="text-lg font-medium text-gray-700 mb-2">
                {{ selectedFile ? selectedFile.name : 'Click to upload your CV' }}
              </p>
              <p class="text-sm text-gray-500">PDF files only, up to 10MB</p>
            </div>
          </div>

          <button
            @click="startAnalysis"
            :disabled="!selectedFile"
            class="bg-orange-500 hover:bg-orange-600 disabled:bg-gray-300 disabled:cursor-not-allowed text-white font-semibold py-3 px-8 rounded-lg transition-colors text-lg"
          >
            Analyze CV
          </button>
        </div>
      </div>

      <!-- Analysis Section -->
      <div v-if="isAnalyzing" class="bg-white rounded-2xl shadow-lg p-8 border border-orange-100">
        <div class="text-center">
          <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-6 animate-spin">
            <svg class="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
          </div>
          
          <h2 class="text-2xl font-bold text-gray-900 mb-4">{{ currentPhrase }}</h2>
          
          <div class="mt-8">
            <button
              @click="showReasoning = !showReasoning"
              class="text-orange-600 hover:text-orange-700 text-sm underline"
            >
              see reasoning
            </button>
            
            <div v-if="showReasoning" class="mt-4 text-left bg-orange-50 rounded-lg p-4">
              <div v-for="(step, index) in reasoningSteps" :key="index" class="flex items-center gap-3 py-2">
                <div class="w-2 h-2 bg-orange-400 rounded-full"></div>
                <span class="text-sm text-gray-700">{{ step }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Section -->
      <div v-if="results" class="space-y-6">
        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-gray-900 mb-2">Analysis Complete!</h2>
          <p class="text-gray-600">Found {{ totalEntities }} medical entities in the CV</p>
        </div>

        <div class="grid gap-6 md:grid-cols-3">
          <div v-for="category in categories" :key="category.name" class="bg-white rounded-2xl shadow-lg border border-orange-100">
            <div class="p-6 border-b border-orange-100">
              <h3 class="text-xl font-bold text-gray-900 mb-2">{{ category.name }}</h3>
              <p class="text-sm text-gray-600">{{ category.count }} found</p>
            </div>
            <div class="p-6 space-y-3">
              <div
                v-for="entity in category.items"
                :key="entity.name"
                @click="selectedEntity = entity"
                class="p-3 bg-orange-50 rounded-lg cursor-pointer hover:bg-orange-100 transition-colors"
              >
                <div class="font-medium text-gray-900">{{ entity.name }}</div>
                <div class="text-sm text-gray-600">{{ entity.type }}</div>
              </div>
            </div>
          </div>
        </div>

        <button
          @click="resetApp"
          class="mx-auto block bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
        >
          Analyze Another CV
        </button>
      </div>

      <!-- Entity Detail Modal -->
      <div v-if="selectedEntity" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50" @click="selectedEntity = null">
        <div class="bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-96 overflow-y-auto" @click.stop>
          <div class="p-6 border-b border-gray-200">
            <div class="flex justify-between items-start">
              <div>
                <h3 class="text-2xl font-bold text-gray-900">{{ selectedEntity.name }}</h3>
                <p class="text-orange-600 font-medium">{{ selectedEntity.type }}</p>
              </div>
              <button @click="selectedEntity = null" class="text-gray-400 hover:text-gray-600">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
              </button>
            </div>
          </div>
          <div class="p-6 space-y-4">
            <div v-for="(value, key) in selectedEntity.details" :key="key">
              <h4 class="font-semibold text-gray-900 capitalize">{{ key.replace(/([A-Z])/g, ' $1') }}</h4>
              <p class="text-gray-600">{{ value }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const selectedFile = ref(null)
const isAnalyzing = ref(false)
const results = ref(null)
const selectedEntity = ref(null)
const showReasoning = ref(false)
const currentPhraseIndex = ref(0)

const phrases = [
  "Our alpacas are analyzing the CV...",
  "Did you know Peruvian alpacas have excellent memory for medical terms?",
  "Scanning for pharmaceutical compounds...",
  "Our lab-coat wearing alpacas are hard at work!",
  "Processing medical terminology with alpaca precision...",
  "Fun fact: Alpacas can identify over 1000 drug compounds!"
]

const reasoningSteps = [
  "Finding exact drug matches",
  "Normalizing tokens with LLM",
  "Checking against vectorstore",
  "Categorizing medical entities",
  "Validating pharmaceutical data"
]

const currentPhrase = computed(() => phrases[currentPhraseIndex.value])

let phraseInterval = null

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file && file.type === 'application/pdf') {
    selectedFile.value = file
  } else {
    alert('Please select a valid PDF file.')
  }
}

const startAnalysis = () => {
  if (!selectedFile.value) return
  
  isAnalyzing.value = true
  showReasoning.value = false
  
  // Start phrase rotation
  phraseInterval = setInterval(() => {
    currentPhraseIndex.value = (currentPhraseIndex.value + 1) % phrases.length
  }, 5000)
  
  // Simulate analysis
  setTimeout(() => {
    isAnalyzing.value = false
    clearInterval(phraseInterval)
    
    results.value = {
      brandDrugs: [
        { name: "Lipitor", type: "Brand Drug", details: { therapeuticClass: "Statin", activeIngredient: "Atorvastatin", indication: "Cholesterol management" }},
        { name: "Advil", type: "Brand Drug", details: { therapeuticClass: "NSAID", activeIngredient: "Ibuprofen", indication: "Pain relief" }}
      ],
      genericDrugs: [
        { name: "Atorvastatin", type: "Generic Drug", details: { therapeuticClass: "Statin", brandNames: "Lipitor, Torvast", indication: "Hypercholesterolemia" }},
        { name: "Metformin", type: "Generic Drug", details: { therapeuticClass: "Biguanide", brandNames: "Glucophage", indication: "Type 2 diabetes" }}
      ],
      ingredients: [
        { name: "Lactose", type: "Excipient", details: { function: "Filler/Binder", commonUse: "Tablet manufacturing", allergenInfo: "May cause issues in lactose intolerant patients" }},
        { name: "Magnesium Stearate", type: "Excipient", details: { function: "Lubricant", commonUse: "Prevents sticking during manufacturing", safetyProfile: "Generally recognized as safe" }}
      ]
    }
  }, 8000)
}

const categories = computed(() => [
  { name: "Brand Drugs", count: results.value?.brandDrugs.length || 0, items: results.value?.brandDrugs || [] },
  { name: "Generic Drugs", count: results.value?.genericDrugs.length || 0, items: results.value?.genericDrugs || [] },
  { name: "Ingredients", count: results.value?.ingredients.length || 0, items: results.value?.ingredients || [] }
])

const totalEntities = computed(() => {
  if (!results.value) return 0
  return results.value.brandDrugs.length + results.value.genericDrugs.length + results.value.ingredients.length
})

const resetApp = () => {
  selectedFile.value = null
  isAnalyzing.value = false
  results.value = null
  selectedEntity.value = null
  showReasoning.value = false
  currentPhraseIndex.value = 0
}

onUnmounted(() => {
  if (phraseInterval) {
    clearInterval(phraseInterval)
  }
})
</script>