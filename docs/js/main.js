
// Userology Help Center - Enhanced Search and Interactivity
let searchIndex = [];
let searchResultsDropdown = null;
let selectedResultIndex = -1;
let searchIndexLoaded = false;

// Determine the base path for loading resources
function getBasePath() {
    const path = window.location.pathname;
    const depth = (path.match(/\//g) || []).length - 1;
    
    if (path.includes('/sections/') || path.includes('/articles/')) {
        return '../';
    }
    return '';
}

const basePath = getBasePath();

// Load search index
fetch(basePath + 'search-index.json')
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        searchIndex = data;
        searchIndexLoaded = true;
        console.log(`✅ Search index loaded: ${searchIndex.length} articles`);
    })
    .catch(err => {
        console.error('❌ Failed to load search index:', err);
        console.log('Make sure search-index.json exists in the same directory');
    });

// Search scoring function
function scoreMatch(item, query) {
    const queryLower = query.toLowerCase();
    const queryWords = queryLower.split(/\s+/).filter(w => w.length > 1);
    let score = 0;
    
    const titleLower = (item.title || '').toLowerCase();
    const sectionLower = (item.section || '').toLowerCase();
    const searchText = (item.searchText || '').toLowerCase();
    
    // Title exact match (highest priority)
    if (titleLower.includes(queryLower)) {
        score += 100;
        // Bonus for match at start
        if (titleLower.startsWith(queryLower)) {
            score += 50;
        }
    }
    
    // Title word matches
    queryWords.forEach(word => {
        if (titleLower.includes(word)) {
            score += 30;
        }
    });
    
    // Section match
    if (sectionLower.includes(queryLower)) {
        score += 20;
    }
    
    queryWords.forEach(word => {
        if (sectionLower.includes(word)) {
            score += 10;
        }
    });
    
    // Content matches
    queryWords.forEach(word => {
        const regex = new RegExp(word, 'gi');
        const matches = (searchText.match(regex) || []).length;
        score += matches * 2;
    });
    
    return score;
}

// Search function
function performSearch(query) {
    if (!query || query.length < 2) return [];
    
    if (!searchIndexLoaded) {
        console.log('⏳ Search index not loaded yet...');
        return [];
    }
    
    console.log(`🔍 Searching for: "${query}"`);
    
    // Score all items
    const results = searchIndex
        .map(item => ({
            ...item,
            score: scoreMatch(item, query)
        }))
        .filter(item => item.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, 10); // Top 10 results
    
    console.log(`📊 Found ${results.length} results`);
    return results;
}

// Highlight matching text
function highlightText(text, query) {
    if (!query) return text;
    const queryWords = query.split(/\s+/).filter(w => w.length > 1);
    let highlighted = text;
    
    queryWords.forEach(word => {
        const regex = new RegExp(`(${word})`, 'gi');
        highlighted = highlighted.replace(regex, '<mark>$1</mark>');
    });
    
    return highlighted;
}

// Create search results dropdown
function createSearchDropdown() {
    if (searchResultsDropdown) {
        console.log('✅ Search dropdown already exists');
        return;
    }
    
    searchResultsDropdown = document.createElement('div');
    searchResultsDropdown.className = 'search-results-dropdown';
    searchResultsDropdown.style.display = 'none';
    
    // Try to find search container (works for both header and hero search)
    let searchContainer = document.querySelector('.search-container');
    if (!searchContainer) {
        searchContainer = document.querySelector('.hero-search');
    }
    
    if (searchContainer) {
        searchContainer.style.position = 'relative';
        searchContainer.appendChild(searchResultsDropdown);
        console.log('✅ Search dropdown created and attached');
    } else {
        console.log('❌ Search container not found');
    }
}

// Show search results in dropdown
function showSearchResults(results, query) {
    if (!searchResultsDropdown) {
        console.log('❌ Search dropdown not initialized');
        return;
    }
    
    selectedResultIndex = -1;
    
    if (!searchIndexLoaded) {
        searchResultsDropdown.innerHTML = '<div class="search-no-results">Loading search index...</div>';
        searchResultsDropdown.style.display = 'block';
        return;
    }
    
    if (results.length === 0) {
        searchResultsDropdown.innerHTML = `
            <div class="search-no-results">
                No results found for "${query}"
                <div style="margin-top: 0.5rem; font-size: 0.875rem;">Try different keywords</div>
            </div>
        `;
        searchResultsDropdown.style.display = 'block';
        return;
    }
    
    let html = '<div class="search-results-list">';
    
    results.forEach((result, index) => {
        const highlightedTitle = highlightText(result.title, query);
        const excerpt = (result.content || '').substring(0, 120) + '...';
        const highlightedExcerpt = highlightText(excerpt, query);
        
        // Fix URL to be relative to current page location
        const resultUrl = basePath + result.url;
        
        html += `
            <a href="${resultUrl}" class="search-result-item" data-index="${index}">
                <div class="search-result-title">${highlightedTitle}</div>
                <div class="search-result-meta">${result.section || 'Unknown'}</div>
                <div class="search-result-excerpt">${highlightedExcerpt}</div>
            </a>
        `;
    });
    
    html += '</div>';
    html += `<div class="search-results-footer"><a href="${basePath}search.html?q=${encodeURIComponent(query)}">See all results →</a></div>`;
    
    searchResultsDropdown.innerHTML = html;
    searchResultsDropdown.style.display = 'block';
    console.log(`✅ Displayed ${results.length} results in dropdown`);
}

// Hide search dropdown
function hideSearchResults() {
    if (searchResultsDropdown) {
        setTimeout(() => {
            searchResultsDropdown.style.display = 'none';
        }, 300); // Increased delay to allow click events to fire
    }
}

// Handle keyboard navigation
function handleSearchKeyboard(e) {
    if (!searchResultsDropdown || searchResultsDropdown.style.display === 'none') return;
    
    const items = searchResultsDropdown.querySelectorAll('.search-result-item');
    
    if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedResultIndex = Math.min(selectedResultIndex + 1, items.length - 1);
        updateSelectedResult(items);
    } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedResultIndex = Math.max(selectedResultIndex - 1, -1);
        updateSelectedResult(items);
    } else if (e.key === 'Enter' && selectedResultIndex >= 0) {
        e.preventDefault();
        items[selectedResultIndex].click();
    } else if (e.key === 'Escape') {
        hideSearchResults();
    }
}

function updateSelectedResult(items) {
    items.forEach((item, index) => {
        if (index === selectedResultIndex) {
            item.classList.add('selected');
            item.scrollIntoView({ block: 'nearest' });
        } else {
            item.classList.remove('selected');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Page loaded, initializing search...');
    
    // Initialize search
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        console.log('✅ Search input found');
        createSearchDropdown();
        
        let searchTimeout;
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            console.log(`⌨️ Input event: "${query}"`);
            
            clearTimeout(searchTimeout);
            
            if (query.length < 2) {
                hideSearchResults();
                return;
            }
            
            // Debounce search
            searchTimeout = setTimeout(() => {
                const results = performSearch(query);
                showSearchResults(results, query);
            }, 150);
        });
        
        searchInput.addEventListener('focus', function(e) {
            const query = e.target.value.trim();
            if (query.length >= 2) {
                console.log('🎯 Focus event with query');
                const results = performSearch(query);
                showSearchResults(results, query);
            }
        });
        
        searchInput.addEventListener('blur', hideSearchResults);
        searchInput.addEventListener('keydown', handleSearchKeyboard);
        
        // Prevent dropdown from closing when clicking on results
        document.addEventListener('mousedown', function(e) {
            if (searchResultsDropdown && searchResultsDropdown.contains(e.target)) {
                e.preventDefault(); // Prevent blur event
            }
        });
        
        // Handle search form submission
        const searchForm = searchInput.closest('form');
        if (searchForm) {
            searchForm.addEventListener('submit', function(e) {
                e.preventDefault();
                const query = searchInput.value.trim();
                if (query) {
                    window.location.href = `${basePath}search.html?q=${encodeURIComponent(query)}`;
                }
            });
        }
    } else {
        console.log('❌ Search input NOT found');
    }
    
    // Add active class to current page navigation
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading states for images (exclude header logo)
    const images = document.querySelectorAll('img:not(.header-logo)');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease';
    });
    
    // Video Carousel functionality
    initVideoCarousel();
    
    // Header transparency on scroll
    initHeaderScroll();
});

function initHeaderScroll() {
    const header = document.querySelector('.header');
    if (!header) return;
    
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    });
}

function initVideoCarousel() {
    const carousel = document.querySelector('.video-carousel');
    if (!carousel) return;
    
    const track = carousel.querySelector('.video-carousel-track');
    const cards = carousel.querySelectorAll('.video-carousel-card');
    const leftArrow = document.querySelector('.carousel-arrow-left');
    const rightArrow = document.querySelector('.carousel-arrow-right');
    
    if (!track || !leftArrow || !rightArrow || cards.length === 0) return;
    
    let currentIndex = 0;
    let cardsPerView = 3;
    
    // Calculate cards per view based on screen width
    function updateCardsPerView() {
        const width = window.innerWidth;
        if (width <= 640) {
            cardsPerView = 1;
        } else if (width <= 900) {
            cardsPerView = 2;
        } else {
            cardsPerView = 3;
        }
        updateCarousel();
    }
    
    // Update carousel position
    function updateCarousel() {
        const cardWidth = cards[0].offsetWidth;
        const gap = 24; // var(--space-6) = 1.5rem = 24px
        const offset = currentIndex * (cardWidth + gap);
        track.style.transform = `translateX(-${offset}px)`;
        
        // Update arrow states
        leftArrow.disabled = currentIndex === 0;
        rightArrow.disabled = currentIndex >= cards.length - cardsPerView;
    }
    
    // Navigation handlers
    leftArrow.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            updateCarousel();
        }
    });
    
    rightArrow.addEventListener('click', () => {
        if (currentIndex < cards.length - cardsPerView) {
            currentIndex++;
            updateCarousel();
        }
    });
    
    // Handle window resize
    let resizeTimeout;
    window.addEventListener('resize', () => {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            currentIndex = 0; // Reset to start on resize
            updateCardsPerView();
        }, 250);
    });
    
    // Make video cards clickable to go to videos page
    cards.forEach((card, index) => {
        card.addEventListener('click', () => {
            window.location.href = 'videos.html';
        });
    });
    
    // Initial setup
    updateCardsPerView();
}
