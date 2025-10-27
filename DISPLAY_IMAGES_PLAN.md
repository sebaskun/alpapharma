# Display Images Implementation Plan

## Simple Google Images Integration (MVP)

### Backend Changes

**1. Add Image Fetching Function** (`utils/image_service.py`)
- Simple function that calls Google Custom Search API
- Search query: `"{drug_name} medication pharmaceutical"`
- Return first image URL or None if error
- No caching, no async - just basic API call

**2. Update Entity Extraction** (`services/pdf_parser.py`)
- Add one line in `scan_text_for_entities()` after finding each entity
- Call image service and add `image_url` field to entity object
- If image fetch fails, set `image_url: null`

**3. Environment Setup**
- Add `GOOGLE_SEARCH_API_KEY` and `CUSTOM_SEARCH_ENGINE_ID` to `.env`
- Add `requests` to requirements.txt if not present

### Frontend Changes

**1. Results Grid** (`App.vue`)
- Add small image thumbnail (60x60px) to each entity card
- Show generic pill icon if `image_url` is null
- Basic `<img>` tag with error handling

**2. Detailed Modal**
- Add image at bottom of modal (300px max width)
- Same fallback logic as grid

### Implementation Details

**Total files to modify**: 4 files
- `utils/image_service.py` (new file, ~20 lines)
- `services/pdf_parser.py` (add 2 lines)
- `.env.example` (add 2 variables)
- `App.vue` (add image display in 2 places)

**No complex features**:
- No image caching
- No async processing
- No loading states
- No retry logic
- Just basic image fetch and display

**Fallback**: Generic pharmaceutical icon for failed/missing images

This keeps it under 1 hour of development time while providing the core image functionality for the MVP.