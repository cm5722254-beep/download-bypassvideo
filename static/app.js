/**
 * TDL Media Downloader Pro - Global Senior Production Edition
 * Master Senior Software Engineering Implementation
 * Real Live API Scrapers • ByteDance VOD Resolver • DramaBox Live Stream • Multi-Threaded Downloader
 */

// Global State
let allItems = [];
let selectedItemIds = new Set();
let currentSource = 'All';
let currentSearch = '';
let activeTasks = [];
let pollInterval = null;
let currentActiveItemForEpisodes = null;

// DOM Elements
const mediaGrid = document.getElementById('mediaGrid');
const emptyState = document.getElementById('emptyState');
const selectAllCheckbox = document.getElementById('selectAllCheckbox');
const selectedCountText = document.getElementById('selectedCountText');
const btnDownloadSelected = document.getElementById('btnDownloadSelected');
const floatingBatchBar = document.getElementById('floatingBatchBar');
const floatingSelectedCount = document.getElementById('floatingSelectedCount');
const btnDeselectAll = document.getElementById('btnDeselectAll');
const searchInput = document.getElementById('searchInput');
const btnClearSearch = document.getElementById('btnClearSearch');
const folderInput = document.getElementById('folderInput');
const btnBrowseFolder = document.getElementById('btnBrowseFolder');
const btnOpenFolder = document.getElementById('btnOpenFolder');
const diskFreeText = document.getElementById('diskFreeText');
const activeTasksBadge = document.getElementById('activeTasksBadge');
const btnLiveScan = document.getElementById('btnLiveScan');
const lastSyncTimeText = document.getElementById('lastSyncTimeText');
const serverStatusText = document.getElementById('serverStatusText');

// Queue Elements
const queueDrawer = document.getElementById('queueDrawer');
const queueOverlay = document.getElementById('queueOverlay');
const btnToggleQueue = document.getElementById('btnToggleQueue');
const btnCloseQueue = document.getElementById('btnCloseQueue');
const btnClearCompleted = document.getElementById('btnClearCompleted');
const queueListContainer = document.getElementById('queueListContainer');
const queueEmptyState = document.getElementById('queueEmptyState');

// Lightbox Elements
const lightboxModal = document.getElementById('lightboxModal');
const lightboxBackdrop = document.getElementById('lightboxBackdrop');
const btnCloseLightbox = document.getElementById('btnCloseLightbox');
const lightboxImage = document.getElementById('lightboxImage');
const lightboxTitle = document.getElementById('lightboxTitle');
const btnLightboxDownloadPoster = document.getElementById('btnLightboxDownloadPoster');

// Episodes Modal Elements
const episodesModal = document.getElementById('episodesModal');
const episodesBackdrop = document.getElementById('episodesBackdrop');
const btnCloseEpisodesModal = document.getElementById('btnCloseEpisodesModal');
const episodesModalCover = document.getElementById('episodesModalCover');
const episodesModalTitle = document.getElementById('episodesModalTitle');
const episodesModalSource = document.getElementById('episodesModalSource');
const episodesModalCount = document.getElementById('episodesModalCount');
const episodesGridContainer = document.getElementById('episodesGridContainer');
const btnDownloadAllEpisodes = document.getElementById('btnDownloadAllEpisodes');

// Player Modal Elements
const playerModal = document.getElementById('playerModal');
const playerBackdrop = document.getElementById('playerBackdrop');
const btnClosePlayerModal = document.getElementById('btnClosePlayerModal');
const playerModalTitle = document.getElementById('playerModalTitle');
const html5VideoPlayer = document.getElementById('html5VideoPlayer');
const btnPlayerDownloadThis = document.getElementById('btnPlayerDownloadThis');

// Custom Direct URL Elements
const tabCustomUrl = document.getElementById('tabCustomUrl');
const customUrlBox = document.getElementById('customUrlBox');
const btnCloseCustomUrl = document.getElementById('btnCloseCustomUrl');
const customUrlInput = document.getElementById('customUrlInput');
const btnParseUrl = document.getElementById('btnParseUrl');

// Batch Options
const checkOptPoster = document.getElementById('checkOptPoster');
const checkOptVideo = document.getElementById('checkOptVideo');
const btnBatchPosterOnly = document.getElementById('btnBatchPosterOnly');
const btnBatchVideoOnly = document.getElementById('btnBatchVideoOnly');
const btnBatchBothFull = document.getElementById('btnBatchBothFull');

const toastContainer = document.getElementById('toastContainer');

// ================= APP INITIALIZATION =================
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    fetchSystemStatus();
    loadCatalog();
    startQueuePolling();
});

function initEventListeners() {
    // Platform Sources Tabs
    document.querySelectorAll('.source-tab').forEach(tab => {
        tab.addEventListener('click', () => {
            if (tab.id === 'tabCustomUrl') {
                customUrlBox.classList.toggle('hidden');
                return;
            }
            document.querySelectorAll('.source-tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentSource = tab.dataset.source;
            renderFilteredGrid();
        });
    });

    // Custom URL Drawer
    btnCloseCustomUrl.addEventListener('click', () => customUrlBox.classList.add('hidden'));
    btnParseUrl.addEventListener('click', handleParseCustomUrl);
    customUrlInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') handleParseCustomUrl();
    });

    // Master Select All Checkbox
    selectAllCheckbox.addEventListener('change', (e) => {
        const visibleItems = getVisibleItems();
        if (e.target.checked) {
            visibleItems.forEach(item => selectedItemIds.add(item.id));
        } else {
            visibleItems.forEach(item => selectedItemIds.delete(item.id));
        }
        updateSelectionUI();
    });

    // Search Box
    searchInput.addEventListener('input', (e) => {
        currentSearch = e.target.value.trim();
        btnClearSearch.classList.toggle('hidden', currentSearch === '');
        renderFilteredGrid();
    });

    btnClearSearch.addEventListener('click', () => {
        searchInput.value = '';
        currentSearch = '';
        btnClearSearch.classList.add('hidden');
        renderFilteredGrid();
    });

    btnDeselectAll.addEventListener('click', () => {
        selectedItemIds.clear();
        updateSelectionUI();
    });

    // Live Server Sync Action
    if (btnLiveScan) {
        btnLiveScan.addEventListener('click', handleLiveServerScan);
    }

    // Windows Native File Explorer Integration
    btnBrowseFolder.addEventListener('click', handleBrowseFolder);
    btnOpenFolder.addEventListener('click', handleOpenFolder);

    // Queue Drawer
    btnToggleQueue.addEventListener('click', () => openQueueDrawer(true));
    btnCloseQueue.addEventListener('click', () => openQueueDrawer(false));
    queueOverlay.addEventListener('click', () => openQueueDrawer(false));
    btnClearCompleted.addEventListener('click', handleClearCompleted);

    // Lightbox Modal
    btnCloseLightbox.addEventListener('click', closeLightbox);
    lightboxBackdrop.addEventListener('click', closeLightbox);

    // Episodes Modal
    btnCloseEpisodesModal.addEventListener('click', closeEpisodesModal);
    episodesBackdrop.addEventListener('click', closeEpisodesModal);

    // Player Modal
    btnClosePlayerModal.addEventListener('click', closePlayerModal);
    playerBackdrop.addEventListener('click', closePlayerModal);

    // Batch Download Actions
    btnDownloadSelected.addEventListener('click', () => {
        const dlPoster = checkOptPoster.checked;
        const dlVideo = checkOptVideo.checked;
        if (!dlPoster && !dlVideo) {
            showToast("សូមជ្រើសរើសប្រភេទ Poster ឬ Video ជាមុនសិន!", "error");
            return;
        }
        executeDownloadForSelected(dlPoster, dlVideo);
    });

    btnBatchPosterOnly.addEventListener('click', () => executeDownloadForSelected(true, false));
    btnBatchVideoOnly.addEventListener('click', () => executeDownloadForSelected(false, true));
    btnBatchBothFull.addEventListener('click', () => executeDownloadForSelected(true, true));
}

// ================= API CALLS =================
async function fetchSystemStatus() {
    try {
        const res = await fetch('/api/status');
        if (res.ok) {
            const data = await res.json();
            folderInput.value = data.download_dir;
            diskFreeText.textContent = `Disk: ${data.disk_free_gb} GB Free`;
            activeTasksBadge.textContent = data.active_downloads;
            if (lastSyncTimeText && data.last_sync_time) {
                lastSyncTimeText.textContent = data.last_sync_time;
            }
        }
    } catch (e) {
        console.error("Status fetch error:", e);
    }
}

async function loadCatalog() {
    try {
        const res = await fetch('/api/catalog');
        if (res.ok) {
            allItems = await res.json();
            updateTabCounts();
            renderFilteredGrid();
        }
    } catch (e) {
        showToast("បរាជ័យក្នុងការទាញយកទិន្នន័យពី Server", "error");
    }
}

function updateTabCounts() {
    const elAll = document.getElementById('tabCountAll');
    const elDb = document.getElementById('tabCountDramaBox');
    const elDonghua = document.getElementById('tabCountDonghua');
    const elIq = document.getElementById('tabCountIqiyi');
    const elHgReal = document.getElementById('tabCountHgReal');
    const elHgComicDrama = document.getElementById('tabCountHgComicDrama');
    const elHgAi = document.getElementById('tabCountHgAi');
    const elHgComic = document.getElementById('tabCountHgComic');

    if (elAll) elAll.textContent = allItems.length;
    if (elDb) elDb.textContent = allItems.filter(x => x.source === 'DramaBox').length;
    if (elDonghua) elDonghua.textContent = allItems.filter(x => x.source === 'Lucifer Donghua').length;
    if (elIq) elIq.textContent = allItems.filter(x => x.source === 'iQIYI').length;
    if (elHgReal) elHgReal.textContent = allItems.filter(x => x.source === 'Hongguo Real Drama').length;
    if (elHgComicDrama) elHgComicDrama.textContent = allItems.filter(x => x.source === 'Hongguo Comic Drama').length;
    if (elHgAi) elHgAi.textContent = allItems.filter(x => x.source === 'Hongguo AI Drama').length;
    if (elHgComic) elHgComic.textContent = allItems.filter(x => x.source === 'Hongguo Comic').length;
}

async function handleLiveServerScan() {
    if (btnLiveScan) {
        btnLiveScan.classList.add('scanning');
        btnLiveScan.querySelector('.scan-btn-text').textContent = 'កំពុងស្កេន API...';
    }
    showToast("📡 កំពុងភ្ជាប់ទៅកាន់ Server API របស់ Hongguo, DramaBox, iQIYI, Donghua...", "info");

    try {
        const res = await fetch('/api/scan-live-servers', { method: 'POST' });
        if (res.ok) {
            const data = await res.json();
            showToast(`✅ ស្កេនជោគជ័យ! ទាញបាន ${data.total_scanned} រឿងពិតៗពី Server (Hongguo: ${data.hongguo_total}, DramaBox: ${data.dramabox_count}, iQIYI: ${data.iqiyi_count}, Donghua: ${data.donghua_count})`, "success");
            await loadCatalog();
            await fetchSystemStatus();
            if (serverStatusText) {
                serverStatusText.textContent = `🟢 ភ្ជាប់ទៅកាន់ Server API ទាំង ៤ ដោយជោគជ័យ (${data.total_scanned} រឿងពិតប្រាកដ)`;
            }
        } else {
            showToast("បរាជ័យក្នុងការស្កេន Server API", "error");
        }
    } catch (e) {
        showToast("បញ្ហាក្នុងការភ្ជាប់ទៅកាន់ Server", "error");
    } finally {
        if (btnLiveScan) {
            btnLiveScan.classList.remove('scanning');
            btnLiveScan.querySelector('.scan-btn-text').textContent = 'ស្កេន Server (Live Sync)';
        }
    }
}

async function handleBrowseFolder() {
    showToast("កំពុងបើកផ្ទាំងជ្រើសរើស Folder ក្នុង Windows...", "info");
    try {
        const res = await fetch('/api/choose-folder-dialog', { method: 'POST' });
        const data = await res.json();
        if (data.status === 'success') {
            folderInput.value = data.folder;
            showToast(`បានកំណត់ទីតាំងរក្សាទុក៖ ${data.folder}`, "success");
        }
    } catch (e) {
        showToast("មិនអាចបើក Folder Dialog បានទេ", "error");
    }
}

async function handleOpenFolder() {
    try {
        const res = await fetch('/api/open-folder');
        const data = await res.json();
        if (data.status === 'success') {
            showToast("បានបើក Folder ក្នុង Windows Explorer", "success");
        } else {
            showToast("មិនអាចបើក Folder បានទេ", "error");
        }
    } catch (e) {
        showToast("បញ្ហាក្នុងការបើក Folder", "error");
    }
}

async function handleParseCustomUrl() {
    const url = customUrlInput.value.trim();
    if (!url) {
        showToast("សូមបញ្ចូល Link វីដេអូ ឬ Poster!", "error");
        return;
    }

    btnParseUrl.disabled = true;
    btnParseUrl.innerHTML = "<span>កំពុងទាញយក...</span>";
    showToast("⚡ កំពុងវិភាគ និងទាញយកទិន្នន័យពី Link...", "info");

    try {
        const res = await fetch('/api/parse-url', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        if (res.ok) {
            const item = await res.json();
            allItems.unshift(item);
            selectedItemIds.add(item.id);
            customUrlInput.value = '';
            customUrlBox.classList.add('hidden');
            updateTabCounts();
            renderFilteredGrid();
            showToast(`បានបន្ថែម "${item.title}" ដោយជោគជ័យ!`, "success");
        } else {
            showToast("Link មិនត្រឹមត្រូវ ឬ Server មិនឆ្លើយតប", "error");
        }
    } catch (e) {
        showToast("បញ្ហាក្នុងការពិនិត្យ Link", "error");
    } finally {
        btnParseUrl.disabled = false;
        btnParseUrl.innerHTML = "<span>⚡ ពិនិត្យ & បញ្ចូល</span>";
    }
}

// ================= RENDER GRID =================
function getVisibleItems() {
    return allItems.filter(item => {
        const matchSource = (currentSource === 'All') || (item.source.toLowerCase() === currentSource.toLowerCase());
        const matchSearch = !currentSearch || (
            item.title.toLowerCase().includes(currentSearch.toLowerCase()) ||
            (item.category && item.category.toLowerCase().includes(currentSearch.toLowerCase())) ||
            (item.description && item.description.toLowerCase().includes(currentSearch.toLowerCase()))
        );
        return matchSource && matchSearch;
    });
}

function renderFilteredGrid() {
    const visibleItems = getVisibleItems();
    mediaGrid.innerHTML = '';

    if (visibleItems.length === 0) {
        emptyState.classList.remove('hidden');
    } else {
        emptyState.classList.add('hidden');
    }

    visibleItems.forEach(item => {
        const isSelected = selectedItemIds.has(item.id);
        const card = document.createElement('div');
        card.className = `media-card ${isSelected ? 'selected' : ''}`;
        card.id = `card-${item.id}`;

        const sourceClass = `badge-${item.source.replace(/\s+/g, '_')}`;

        card.innerHTML = `
            <div class="card-poster-wrapper">
                <img class="card-poster-img" src="${item.poster_url}" alt="${item.title}" loading="lazy" onerror="this.src='https://images.unsplash.com/photo-1579546929518-9e396f3cc809?auto=format&fit=crop&w=400&q=80'">
                <div class="card-poster-gradient"></div>

                <div class="card-checkbox-wrap">
                    <label class="card-select-label" onclick="event.stopPropagation()">
                        <input type="checkbox" class="item-checkbox" data-id="${item.id}" ${isSelected ? 'checked' : ''}>
                        <span class="custom-checkbox"></span>
                    </label>
                </div>

                <div class="card-badges-wrap">
                    <span class="badge-source ${sourceClass}">${item.source}</span>
                    <span class="badge-quality">${item.quality || '1080P'}</span>
                </div>

                <button class="card-preview-btn" title="មើលរូបភាព Poster កម្រិត HD ធំ" onclick="openLightbox('${item.id}'); event.stopPropagation();">
                    👁️
                </button>
            </div>

            <div class="card-details">
                <div class="card-meta-row">
                    <span>${item.category || 'Drama'}</span>
                    <span>${item.episodes ? item.episodes + ' ភាគ (Eps)' : 'Direct'}</span>
                </div>
                <h3 class="card-title" title="${item.title}">${item.title}</h3>
                <p class="card-desc">${item.description || ''}</p>

                <!-- Professional Master Actions -->
                <div class="card-actions-trio">
                    <button class="btn-card-action-sm btn-act-episodes" title="មើលបញ្ជីភាគទាំងអស់" onclick="openEpisodesModal('${item.id}')">
                        <span>🎬 ភាគ (${item.episodes || 1})</span>
                    </button>
                    <button class="btn-card-action-sm btn-act-play" id="btnPlayCard-${item.id}" title="ចាក់វីដេអូមើលក្នុង Tool ពី Server API ផ្ទាល់" onclick="openPlayerModal('${item.id}')">
                        <span>▶️ ចាក់មើល</span>
                    </button>
                    <button class="btn-card-action-sm btn-act-video" title="ទាញយក Video 1080P ចូល Folder" onclick="downloadSingleItem('${item.id}', false, true)">
                        <span>⬇️ Video</span>
                    </button>
                    <button class="btn-card-action-sm btn-act-poster" title="ទាញយក Poster HD ចូល Folder" onclick="downloadSingleItem('${item.id}', true, false)">
                        <span>🖼️ Poster</span>
                    </button>
                </div>

                <!-- Mini Progress Bar inside card -->
                <div class="card-progress-box hidden" id="cardProgressBox-${item.id}">
                    <div class="card-progress-bar">
                        <div class="card-progress-fill animated-stripes" id="cardProgressFill-${item.id}"></div>
                    </div>
                    <div class="card-progress-info">
                        <span id="cardProgressLabel-${item.id}">កំពុងទាញយក...</span>
                        <span id="cardProgressPercent-${item.id}">0%</span>
                    </div>
                </div>
            </div>
        `;

        // Card checkbox click handler
        const chk = card.querySelector('.item-checkbox');
        chk.addEventListener('change', (e) => {
            if (e.target.checked) {
                selectedItemIds.add(item.id);
            } else {
                selectedItemIds.delete(item.id);
            }
            updateSelectionUI();
        });

        // Click on poster thumbnail toggles checkbox
        const posterWrap = card.querySelector('.card-poster-wrapper');
        posterWrap.addEventListener('click', (e) => {
            if (e.target.closest('.card-preview-btn') || e.target.closest('.card-checkbox-wrap')) return;
            chk.checked = !chk.checked;
            chk.dispatchEvent(new Event('change'));
        });

        mediaGrid.appendChild(card);
    });

    updateSelectionUI();
}

// ================= SELECTION MANAGEMENT =================
function updateSelectionUI() {
    const visibleItems = getVisibleItems();
    const count = selectedItemIds.size;

    const allVisibleSelected = visibleItems.length > 0 && visibleItems.every(item => selectedItemIds.has(item.id));
    selectAllCheckbox.checked = allVisibleSelected;

    selectedCountText.textContent = `${count} បានជ្រើសរើស`;
    floatingSelectedCount.textContent = count;

    visibleItems.forEach(item => {
        const card = document.getElementById(`card-${item.id}`);
        if (card) {
            const isSel = selectedItemIds.has(item.id);
            card.classList.toggle('selected', isSel);
            const chk = card.querySelector('.item-checkbox');
            if (chk) chk.checked = isSel;
        }
    });

    if (count > 0) {
        btnDownloadSelected.classList.remove('disabled');
        btnDownloadSelected.removeAttribute('disabled');
        floatingBatchBar.classList.remove('hidden');
    } else {
        btnDownloadSelected.classList.add('disabled');
        btnDownloadSelected.setAttribute('disabled', 'true');
        floatingBatchBar.classList.add('hidden');
    }
}

// ================= EPISODES BREAKDOWN MODAL =================
async function openEpisodesModal(itemId) {
    const item = allItems.find(i => i.id === itemId);
    if (!item) return;
    currentActiveItemForEpisodes = item;

    episodesModalCover.src = item.poster_url;
    episodesModalTitle.textContent = item.title;
    episodesModalSource.textContent = item.source;
    episodesModalCount.textContent = `Total: ${item.episodes || 1} ភាគ (Episodes)`;

    episodesGridContainer.innerHTML = '<div style="color:var(--text-muted); padding:20px; text-align:center;">📡 កំពុងទាញយកទិន្នន័យភាគពិតៗពី Server API...</div>';
    episodesModal.classList.remove('hidden');

    try {
        const res = await fetch(`/api/episodes/${itemId}`);
        if (res.ok) {
            const data = await res.json();
            renderEpisodesGrid(data.episodes, item);
        } else {
            episodesGridContainer.innerHTML = '<div style="color:var(--accent-rose); padding:20px; text-align:center;">មិនអាចទាញយកភាគបានទេ</div>';
        }
    } catch (e) {
        episodesGridContainer.innerHTML = '<div style="color:var(--accent-rose); padding:20px; text-align:center;">បញ្ហាបណ្តាញ</div>';
    }

    btnDownloadAllEpisodes.onclick = () => {
        downloadSingleItem(item.id, true, true);
        closeEpisodesModal();
    };
}

function renderEpisodesGrid(episodes, item) {
    episodesGridContainer.innerHTML = '';
    episodes.forEach(ep => {
        const card = document.createElement('div');
        card.className = 'episode-card';
        card.innerHTML = `
            <div class="ep-top-row">
                <span class="ep-num">${ep.title}</span>
                <span class="ep-quality">${ep.quality}</span>
            </div>
            <div class="ep-duration">ថិរវេលា៖ ${ep.duration}</div>
            <div class="ep-actions-row" style="display:flex; gap:8px; margin-top:8px;">
                <button class="btn-dl-single-ep" style="flex:1;" onclick="playDirectStream('${item.title} - ${ep.title}', '${ep.video_url || ''}', '${item.id}')">
                    <span>▶️ ចាក់មើល</span>
                </button>
                <button class="btn-dl-single-ep" style="flex:1; background:var(--primary-gradient);" onclick="downloadSingleEpisode('${item.id}', ${ep.episode_number})">
                    <span>⬇️ ទាញយក</span>
                </button>
            </div>
        `;
        episodesGridContainer.appendChild(card);
    });
}

function downloadSingleEpisode(itemId, epNumber) {
    const item = allItems.find(i => i.id === itemId);
    if (!item) return;

    const singleEpItem = {
        ...item,
        title: `${item.title} - Ep ${epNumber}`
    };

    downloadSingleItemCustom(singleEpItem, false, true);
    showToast(`កំពុងទាញយកភាគ ${epNumber}...`, "info");
}

function closeEpisodesModal() {
    episodesModal.classList.add('hidden');
}

// ================= BUILT-IN VIDEO PLAYER MODAL =================
async function openPlayerModal(itemId) {
    const item = allItems.find(i => i.id === itemId);
    if (!item) return;

    playerModalTitle.textContent = `[កំពុងភ្ជាប់ Server...] ${item.title}`;
    const hostTag = document.querySelector('.player-quality-info');
    if (hostTag) {
        hostTag.innerHTML = `<span>កម្រិតរូបភាព៖ <strong>1080P FHD (Live)</strong></span> <span>ប្រភព Server៖ <strong>កំពុងភ្ជាប់...</strong></span>`;
    }

    playerModal.classList.remove('hidden');

    // Show loading indicator in video player
    html5VideoPlayer.pause();
    html5VideoPlayer.src = '';

    try {
        // Dynamically resolve real live stream from server host
        const res = await fetch(`/api/resolve-stream/${itemId}`);
        if (res.ok) {
            const data = await res.json();
            playerModalTitle.textContent = data.title || item.title;
            if (hostTag) {
                hostTag.innerHTML = `<span>កម្រិតរូបភាព៖ <strong>${data.quality || '1080P FHD'}</strong></span> <span>ប្រភព Server៖ <strong style="color:var(--accent-emerald);">🟢 ${data.stream_host || 'Official CDN'}</strong></span>`;
            }

            if (data.video_url) {
                html5VideoPlayer.src = data.video_url;
                html5VideoPlayer.load();
                html5VideoPlayer.play().catch(() => {});
            } else {
                showToast("Server មិនទាន់ផ្តល់ Stream URL ឡើយ", "error");
            }
        } else {
            showToast("មិនអាច Resolve Video Stream បានទេ", "error");
        }
    } catch (e) {
        showToast("បញ្ហាក្នុងការភ្ជាប់ទៅកាន់ Video Stream", "error");
    }

    btnPlayerDownloadThis.onclick = () => {
        downloadSingleItem(item.id, true, true);
        closePlayerModal();
    };
}

function playDirectStream(title, url, itemId) {
    if (!url) {
        openPlayerModal(itemId);
        return;
    }
    playerModalTitle.textContent = title;
    html5VideoPlayer.src = url;
    html5VideoPlayer.load();
    html5VideoPlayer.play().catch(() => {});
    playerModal.classList.remove('hidden');

    btnPlayerDownloadThis.onclick = () => {
        downloadSingleItem(itemId, true, true);
        closePlayerModal();
    };
}

function closePlayerModal() {
    html5VideoPlayer.pause();
    html5VideoPlayer.src = '';
    playerModal.classList.add('hidden');
}

// ================= DOWNLOAD EXECUTION =================
async function downloadSingleItem(itemId, dlPoster, dlVideo) {
    const item = allItems.find(i => i.id === itemId);
    if (!item) return;
    downloadSingleItemCustom(item, dlPoster, dlVideo);
}

async function downloadSingleItemCustom(item, dlPoster, dlVideo) {
    showToast(`ចាប់ផ្តើមទាញយក "${item.title.substring(0, 24)}..."`, "info");
    showCardProgress(item.id, true);
    openQueueDrawer(true);

    try {
        const res = await fetch('/api/download/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                items: [item],
                download_posters: dlPoster,
                download_videos: dlVideo
            })
        });
        if (res.ok) {
            showToast("បានបញ្ជូនកិច្ចការទាញយកទៅកាន់ Queue!", "success");
        }
    } catch (e) {
        showToast("បរាជ័យក្នុងការចាប់ផ្តើម Download", "error");
        showCardProgress(item.id, false);
    }
}

async function executeDownloadForSelected(dlPoster, dlVideo) {
    const selectedList = allItems.filter(item => selectedItemIds.has(item.id));
    if (selectedList.length === 0) {
        showToast("សូមជ្រើសរើសវីដេអូ ឬ Poster យ៉ាងហោចណាស់ ១!", "error");
        return;
    }

    showToast(`កំពុងចាប់ផ្ដើមទាញយក ${selectedList.length} ឯកសារក្នុងពេលតែមួយ...`, "info");
    openQueueDrawer(true);

    selectedList.forEach(item => showCardProgress(item.id, true));

    try {
        const res = await fetch('/api/download/start', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                items: selectedList,
                download_posters: dlPoster,
                download_videos: dlVideo
            })
        });
        if (res.ok) {
            showToast(`បានចាប់ផ្ដើមទាញយក ${selectedList.length} ឯកសារដោយជោគជ័យ!`, "success");
            selectedItemIds.clear();
            updateSelectionUI();
        }
    } catch (e) {
        showToast("បរាជ័យក្នុងការបញ្ជូនកិច្ចការទាញយក", "error");
    }
}

function showCardProgress(itemId, show) {
    const box = document.getElementById(`cardProgressBox-${itemId}`);
    if (box) box.classList.toggle('hidden', !show);
}

// ================= QUEUE POLLING & RENDER =================
function startQueuePolling() {
    pollInterval = setInterval(async () => {
        try {
            const res = await fetch('/api/download/tasks');
            if (res.ok) {
                activeTasks = await res.json();
                renderQueueDrawer();
                updateCardProgressFromTasks();
                fetchSystemStatus();
            }
        } catch (e) {
            console.error("Queue poll error:", e);
        }
    }, 800);
}

function renderQueueDrawer() {
    if (activeTasks.length === 0) {
        queueEmptyState.classList.remove('hidden');
        queueListContainer.innerHTML = '';
        queueListContainer.appendChild(queueEmptyState);
        return;
    }

    queueEmptyState.classList.add('hidden');
    queueListContainer.innerHTML = '';

    activeTasks.forEach(task => {
        const card = document.createElement('div');
        card.className = `queue-task-card ${task.status}`;

        const isCompleted = task.status === 'completed';
        const isDownloading = task.status === 'downloading';

        card.innerHTML = `
            <div class="task-top-row">
                <span class="task-title" title="${task.title}">${task.title}</span>
                <span class="task-speed-badge">${task.speed}</span>
            </div>
            <div class="task-file-label">${task.current_file || ''}</div>
            <div class="task-progress-track">
                <div class="task-progress-fill ${isCompleted ? 'completed' : ''}" style="width: ${task.progress}%"></div>
            </div>
            <div class="task-bottom-row">
                <span>${task.progress}% ${isCompleted ? '• រួចរាល់ (' + task.completed_time + ')' : ''}</span>
                <div class="task-actions-wrap">
                    ${isCompleted ? `
                        <button class="btn-task-action open-folder" onclick="openTaskFolder('${task.id}')">
                            📂 បើក Folder
                        </button>
                    ` : ''}
                    ${isDownloading ? `
                        <button class="btn-task-action" onclick="cancelTask('${task.id}')">
                            ✕ បោះបង់
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
        queueListContainer.appendChild(card);
    });
}

function updateCardProgressFromTasks() {
    activeTasks.forEach(task => {
        if (!task.item_id) return;
        const fill = document.getElementById(`cardProgressFill-${task.item_id}`);
        const percent = document.getElementById(`cardProgressPercent-${task.item_id}`);
        const label = document.getElementById(`cardProgressLabel-${task.item_id}`);
        const box = document.getElementById(`cardProgressBox-${task.item_id}`);

        if (fill && percent && box) {
            box.classList.remove('hidden');
            fill.style.width = `${task.progress}%`;
            percent.textContent = `${task.progress}%`;
            if (label) label.textContent = task.speed;

            if (task.status === 'completed') {
                if (label) label.textContent = 'រួចរាល់ 100%';
                setTimeout(() => {
                    box.classList.add('hidden');
                }, 3000);
            }
        }
    });
}

async function cancelTask(taskId) {
    try {
        await fetch(`/api/download/cancel/${taskId}`, { method: 'POST' });
        showToast("បានបោះបង់កិច្ចការទាញយក", "info");
    } catch (e) {
        console.error(e);
    }
}

async function openTaskFolder(taskId) {
    try {
        await fetch(`/api/download/open-task-folder/${taskId}`, { method: 'POST' });
    } catch (e) {
        showToast("មិនអាចបើក Folder បានទេ", "error");
    }
}

async function handleClearCompleted() {
    try {
        await fetch('/api/download/clear-completed', { method: 'POST' });
        showToast("បានសំអាតកិច្ចការដែលបានបញ្ចប់", "success");
    } catch (e) {
        console.error(e);
    }
}

function openQueueDrawer(open) {
    queueDrawer.classList.toggle('hidden', !open);
    queueOverlay.classList.toggle('hidden', !open);
}

// ================= LIGHTBOX PREVIEW =================
function openLightbox(itemId) {
    const item = allItems.find(i => i.id === itemId);
    if (!item) return;

    lightboxImage.src = item.poster_url;
    lightboxTitle.textContent = item.title;
    lightboxModal.classList.remove('hidden');

    btnLightboxDownloadPoster.onclick = () => {
        downloadSingleItem(item.id, true, false);
        closeLightbox();
    };
}

function closeLightbox() {
    lightboxModal.classList.add('hidden');
}

// ================= TOAST NOTIFICATIONS =================
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    let icon = '⚡';
    if (type === 'success') icon = '✅';
    else if (type === 'error') icon = '⚠️';

    toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3200);
}
