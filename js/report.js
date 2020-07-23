let videoSelected = "qp";
let videoCurrentTime = 0;
let videos = document.getElementsByClassName("vis-video");


const add_video_event_listener = () => {
    Array.from(videos).forEach((video) => {
        video.addEventListener("play", () => {
            Array.from(videos).forEach((video) => {
                video.play();
            });
        });
        video.addEventListener("pause", () => {
            Array.from(videos).forEach((video) => {
                video.pause();
            });
            videoCurrentTime = video.currentTime;
            // in case of playback delay
            update_current_time();
            update_frame_detail_page();
        });
        video.addEventListener("seeking", () => {
            if (video.currentTime === videoCurrentTime) return;
            videoCurrentTime = video.currentTime;
            update_current_time();
            update_frame_detail_page();
        });
    });
}
add_video_event_listener();


const update_current_time = () => {
    Array.from(videos).forEach((video) => {
        video.currentTime = videoCurrentTime;
    });
}


document.getElementById("nxt-frame-btn").addEventListener("click", () => {
    let currentTime = videoCurrentTime;
    let offset = 0.00001;
    console.log("current time: " + currentTime);
    for (let i = 0; i < frame_ts.length; i++) {
        if (frame_ts[i] > currentTime) {
            videos[0].currentTime = Number(frame_ts[i]) + offset;
            break;
        }
    }
});


document.getElementById("pre-frame-btn").addEventListener("click", () => {
    let currentTime = videoCurrentTime;
    let offset = -0.00001;
    console.log("current time: " + currentTime);
    for (let i = frame_ts.length - 1; i >= 0; i--) {
        if (frame_ts[i] < currentTime) {
            videos[0].currentTime = Number(frame_ts[i]) + offset;
            break;
        }
    }
});


const get_cur_frame_idx = () => {
    for (let i = 0; i < frame_ts.length; i++) {
        if (frame_ts[i] > videoCurrentTime) {
            return i - 1;
        }
    }
    return frame_ts.length - 1;
}


update_frame_detail_page = () => {
    let frame_idx = get_cur_frame_idx();
    document.getElementById("fd-pts").innerText = frame_map[frame_idx].pts_time;
    document.getElementById("fd-fmt").innerText = frame_map[frame_idx].fmt;
    document.getElementById("fd-qp").innerText = frame_map[frame_idx].qp;
    document.getElementById("fd-type").innerText = frame_map[frame_idx].type;
    document.getElementById("fd-key").innerText = frame_map[frame_idx].iskey === "0" ? "False" : "True";
    document.getElementById("fd-checksum").innerText = frame_map[frame_idx].checksum;
}


document.getElementById("frame-detail-btn").addEventListener("click", () => {
    let frameDetailContainer = document.getElementById("frame-detail-container");
    let dis = frameDetailContainer.style.display;
    frameDetailContainer.style.display = (!dis || dis === "none") ? "block" : "none";
});


let videoSelector = document.getElementById("video-selector")
videoSelector.addEventListener("change", () => {
    let qpVideoContainer = document.getElementById("qp-video-container");
    let mvVideoContainer = document.getElementById("mv-video-container");
    let bsVideoContainer = document.getElementById("bs-video-container");
    let mbTypeVideoContainer = document.getElementById("mb-type-video-container");
    videoSelected = videoSelector.value;
    qpVideoContainer.style.display = "none";
    mvVideoContainer.style.display = "none";
    bsVideoContainer.style.display = "none";
    mbTypeVideoContainer.style.display = "none";
    switch (videoSelector.value) {
        case "qp":
            qpVideoContainer.style.display = "block";
            break;
        case "mv":
            mvVideoContainer.style.display = "block";
            break;
        case "bs":
            bsVideoContainer.style.display = "block";
            break;
        case "mb-type":
            mbTypeVideoContainer.style.display = "block";
            break;
    }
});


/**
 * Event handler for previous or next frame keyboard shortcut
 * @param e event
 */
const doc_keyUp = e => {
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