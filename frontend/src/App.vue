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
        <div class="flex justify-center mb-6">
          <img src="./assets/alpapharma_transparent.png" alt="AlpaPharma Logo" class="h-40 w-auto">
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

        <div class="grid gap-6 md:grid-cols-2">
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
            <div v-if="selectedEntity.details.message === 'adjustment needed'">
              <p class="text-red-600 font-semibold mb-4">adjustment needed</p>
              <pre class="bg-gray-100 p-4 rounded-lg text-sm overflow-auto whitespace-pre-wrap">{{ JSON.stringify(selectedEntity.details.rawData, null, 2) }}</pre>
            </div>
            <div v-else-if="selectedEntity.type === 'Ingredient'">
              <!-- Ingredient Details -->
              <div class="space-y-4">
                <div>
                  <h4 class="font-semibold text-gray-900 mb-2">Ingredient Name</h4>
                  <p class="text-gray-700">{{ selectedEntity.name }}</p>
                </div>

                <div v-if="selectedEntity.details && typeof selectedEntity.details === 'object'">
                  <h4 class="font-semibold text-gray-900 mb-3">Found in</h4>
                  <div class="bg-orange-50 p-4 rounded-lg space-y-3">
                    <div v-if="selectedEntity.details.brand_name">
                      <span class="font-medium text-gray-600">Brand Name:</span>
                      <span class="ml-2">{{ selectedEntity.details.brand_name }}</span>
                    </div>
                    <div v-if="selectedEntity.details.product_ndc">
                      <span class="font-medium text-gray-600">Product NDC:</span>
                      <span class="ml-2">{{ selectedEntity.details.product_ndc }}</span>
                    </div>
                    <div v-if="selectedEntity.details.labeler_name">
                      <span class="font-medium text-gray-600">Labeler:</span>
                      <span class="ml-2">{{ selectedEntity.details.labeler_name }}</span>
                    </div>
                    <div v-if="selectedEntity.details.openfda?.manufacturer_name?.length">
                      <span class="font-medium text-gray-600">Manufacturer:</span>
                      <span class="ml-2">{{ selectedEntity.details.openfda.manufacturer_name.join(', ') }}</span>
                    </div>
                    <div v-if="selectedEntity.details.product_type">
                      <span class="font-medium text-gray-600">Product Type:</span>
                      <span class="ml-2">{{ selectedEntity.details.product_type }}</span>
                    </div>
                    <div v-if="selectedEntity.details.route?.length">
                      <span class="font-medium text-gray-600">Route:</span>
                      <span class="ml-2">{{ selectedEntity.details.route.join(', ') }}</span>
                    </div>
                    <div v-if="selectedEntity.details.dosage_form">
                      <span class="font-medium text-gray-600">Dosage Form:</span>
                      <span class="ml-2">{{ selectedEntity.details.dosage_form }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else>
              <!-- Drug Details -->
              <div class="space-y-4">
                <div>
                  <h4 class="font-semibold text-gray-900 mb-2">Name</h4>
                  <p class="text-gray-700">{{ selectedEntity.name }}</p>
                </div>

                <div v-if="selectedEntity.details && typeof selectedEntity.details === 'object'">
                  <div class="grid gap-4">
                    <div v-if="selectedEntity.details.product_ndc" class="border-b border-gray-100 pb-2">
                      <span class="font-medium text-gray-600">Product NDC:</span>
                      <span class="ml-2">{{ selectedEntity.details.product_ndc }}</span>
                    </div>

                    <div v-if="selectedEntity.details.labeler_name" class="border-b border-gray-100 pb-2">
                      <span class="font-medium text-gray-600">Labeler Name:</span>
                      <span class="ml-2">{{ selectedEntity.details.labeler_name }}</span>
                    </div>

                    <div v-if="selectedEntity.details.brand_name" class="border-b border-gray-100 pb-2">
                      <span class="font-medium text-gray-600">Brand Name:</span>
                      <span class="ml-2">{{ selectedEntity.details.brand_name }}</span>
                    </div>

                    <div v-if="selectedEntity.details.active_ingredients?.length" class="border-b border-gray-100 pb-2">
                      <span class="font-medium text-gray-600">Active Ingredients:</span>
                      <div class="ml-2 mt-1">
                        <div v-for="ingredient in selectedEntity.details.active_ingredients" :key="ingredient.name" class="text-sm">
                          <span class="font-medium">{{ ingredient.name }}</span>
                          <span v-if="ingredient.strength" class="text-gray-500 ml-1">({{ ingredient.strength }})</span>
                        </div>
                      </div>
                    </div>

                    <div v-if="selectedEntity.details.openfda?.manufacturer_name?.length" class="border-b border-gray-100 pb-2">
                      <span class="font-medium text-gray-600">Manufacturer:</span>
                      <span class="ml-2">{{ selectedEntity.details.openfda.manufacturer_name.join(', ') }}</span>
                    </div>

                    <div v-if="selectedEntity.details.product_type" class="border-b border-gray-100 pb-2">
                      <span class="font-medium text-gray-600">Product Type:</span>
                      <span class="ml-2">{{ selectedEntity.details.product_type }}</span>
                    </div>

                    <div v-if="selectedEntity.details.route?.length" class="border-b border-gray-100 pb-2">
                      <span class="font-medium text-gray-600">Route:</span>
                      <span class="ml-2">{{ selectedEntity.details.route.join(', ') }}</span>
                    </div>

                    <div v-if="selectedEntity.details.dosage_form" class="border-b border-gray-100 pb-2">
                      <span class="font-medium text-gray-600">Dosage Form:</span>
                      <span class="ml-2">{{ selectedEntity.details.dosage_form }}</span>
                    </div>
                  </div>
                </div>
              </div>
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

const startAnalysis = async () => {
  if (!selectedFile.value) return

  isAnalyzing.value = true
  showReasoning.value = false

  // Start phrase rotation
  phraseInterval = setInterval(() => {
    currentPhraseIndex.value = (currentPhraseIndex.value + 1) % phrases.length
  }, 5000)

  try {
    // Prepare the request
    const formData = new FormData()
    formData.append('file', selectedFile.value)

    console.log('Request - Uploading file:', {
      name: selectedFile.value.name,
      size: selectedFile.value.size,
      type: selectedFile.value.type
    })

    // Call the backend API
    const response = await fetch('http://localhost:8000/extract', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    console.log('Response - Extracted entities:', data)

    // Transform the response to match the new structure
    const entities = data.search || []
    const drugs = []
    const ingredients = []

    entities.forEach(entity => {
      // Handle malformed objects where info is not a dictionary
      if (!entity.info || typeof entity.info !== 'object' || Array.isArray(entity.info)) {
        // Add to drugs with adjustment needed message
        drugs.push({
          name: entity.name || 'Unknown',
          type: 'Drug',
          details: { message: 'adjustment needed', rawData: entity }
        })
        return
      }

      // Properly structured entity
      if (entity.info.is_ingredient) {
        ingredients.push({
          name: entity.name,
          type: 'Ingredient',
          details: entity.info.record || entity.info
        })
      } else {
        drugs.push({
          name: entity.name,
          type: 'Drug',
          details: entity.info.record || entity.info
        })
      }
    })

    results.value = {
      drugs: drugs,
      ingredients: ingredients
    }

  } catch (error) {
    console.error('Error calling /extract endpoint:', error)
    alert('An error occurred while analyzing the CV. Please try again.')
  } finally {
    isAnalyzing.value = false
    clearInterval(phraseInterval)
  }
}

const categories = computed(() => [
  { name: "Drugs", count: results.value?.drugs.length || 0, items: results.value?.drugs || [] },
  { name: "Ingredients", count: results.value?.ingredients.length || 0, items: results.value?.ingredients || [] }
])

const totalEntities = computed(() => {
  if (!results.value) return 0
  return results.value.drugs.length + results.value.ingredients.length
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