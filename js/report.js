let videoSelected = "qp";
let videoSuffix = "-video";


document.getElementById("nxt-frame-btn").addEventListener("click", () => {
    let videoId = videoSelected + videoSuffix;
    let vid = document.getElementById(videoId);
    let currentTime = vid.currentTime;
    let offset = 0.00001;
    console.log("current time: " + currentTime);
    for (let i = 0; i < frame_ts.length; i++) {
        if (frame_ts[i] > currentTime) {
            vid.currentTime = Number(frame_ts[i]) + offset;
            break;
        }
    }
});

document.getElementById("pre-frame-btn").addEventListener("click", () => {
    let videoId = videoSelected + videoSuffix;
    let vid = document.getElementById(videoId);
    let currentTime = vid.currentTime;
    let offset = -0.00001;
    console.log("current time: " + currentTime);
    for (let i = frame_ts.length - 1; i >= 0; i--) {
        if (frame_ts[i] < currentTime) {
            vid.currentTime = Number(frame_ts[i]) + offset;
            break;
        }
    }
});

let videoSelector = document.getElementById("video-selector")
videoSelector.addEventListener("change", () => {
    let qpVideoContainer = document.getElementById("qp-video-container");
    let bsVideoContainer = document.getElementById("bs-video-container");
    let mbTypeVideoContainer = document.getElementById("mb-type-video-container");
    videoSelected = videoSelector.value;
    qpVideoContainer.style.display = "none";
    bsVideoContainer.style.display = "none";
    mbTypeVideoContainer.style.display = "none";
    if (videoSelector.value === "qp") {
        qpVideoContainer.style.display = "block";
    } else if (videoSelector.value === "bs") {
        bsVideoContainer.style.display = "block";
    } else if (videoSelector.value === "mb-type") {
        mbTypeVideoContainer.style.display = "block";
    }
});

/**
 * Event handler for previous or next frame keyboard shortcut
 * @param e event
 */
function doc_keyUp(e) {
    switch (e.key) {
        case ",":
            document.getElementById("pre-frame-btn").click();
            break;
        case ".":
            document.getElementById("nxt-frame-btn").click();
            break;
    }
}

// register the handler
document.addEventListener('keyup', doc_keyUp, false);