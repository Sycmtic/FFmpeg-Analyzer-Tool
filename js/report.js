let numFramePerFile = 10;
let videoSelected = "qp";
let videoCurrentTime = 0;
let videos = document.getElementsByClassName("vis-video");
let showBlockDetail = false;
let offset = 0.001 /* offset between pst_start and pts to be set */


/**
 * Add event listener to videos
 */
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
            let f_idx = get_cur_frame_idx("vis");
            video.currentTime = Number(frame_ts[f_idx]) + offset;
            videoCurrentTime = video.currentTime;
            update_current_time();
            update_frame_detail_page();
            if (showBlockDetail) {
                remove_block_overlay();
                create_block_overlay();
            }
        });
    });
}
add_video_event_listener();


/**
 * Sync the current time of all visualization videos
 */
const update_current_time = () => {
    Array.from(videos).forEach((video) => {
        video.currentTime = videoCurrentTime;
    });
}


/**
 * Add event listener to button bar
 */
const add_button_bar_listener = () => {
    document.getElementById("nxt-frame-btn").addEventListener("click", () => {
        let currentTime = videoCurrentTime;
        for (let i = 0; i < frame_ts.length; i++) {
            if (frame_ts[i] > currentTime) {
                videos[0].currentTime = Number(frame_ts[i]) + offset;
                console.log("current time: " + videos[0].currentTime);
                break;
            }
        }
    });

    document.getElementById("pre-frame-btn").addEventListener("click", () => {
        let currentTime = videoCurrentTime;
        for (let i = frame_ts.length - 1; i >= 1; i--) {
            if (frame_ts[i] < currentTime) {
                videos[0].currentTime = Number(frame_ts[i - 1]) + offset;
                console.log("current time: " + videos[0].currentTime);
                break;
            }
        }
    });

    document.getElementById("block-detail-btn").addEventListener("click", () => {
        let blockDetailContainer = document.getElementById("block-detail-container");
        let overlayContainer = document.getElementById("overlay-container");
        showBlockDetail = !showBlockDetail;
        blockDetailContainer.style.display = showBlockDetail ? "block" : "none";
        overlayContainer.style.display = showBlockDetail ? "block" : "none";
        Array.from(videos).forEach((video) => {
            video.controls = !showBlockDetail;
        });
        if (showBlockDetail) {
            create_block_overlay();
        } else {
            remove_block_overlay();
        }
    });

    document.getElementById("frame-detail-btn").addEventListener("click", () => {
        let frameDetailContainer = document.getElementById("frame-detail-container");
        let dis = frameDetailContainer.style.display;
        frameDetailContainer.style.display = (!dis || dis === "none") ? "block" : "none";
    });
}
add_button_bar_listener();


/**
 * Get the index of current paused frame
 *
 * @param {string} type of video (vis or ssim)
 * @return {number} frame index
 */
const get_cur_frame_idx = (type) => {
    let currentTime;
    switch (type) {
        case 'vis':
            currentTime = videoCurrentTime;
            break;
        case 'ssim':
            currentTime = ssimVideoCurrentTime;
            break;
        default:
            return -1;
    }
    for (let i = 0; i < frame_ts.length; i++) {
        if (frame_ts[i] > currentTime) {
            return i - 1;
        }
    }
    return frame_ts.length - 1;
}


/**
 * Update the frame detail plane to current frame
 */
update_frame_detail_page = () => {
    let frame_idx = get_cur_frame_idx("vis");
    document.getElementById("fd-pts-time").innerText = frame_map[frame_idx].pkt_pts_time;
    document.getElementById("fd-pts").innerText = frame_map[frame_idx].pkt_pts;
    document.getElementById("fd-dts").innerText = frame_map[frame_idx].pkt_dts;
    document.getElementById("fd-type").innerText = frame_map[frame_idx].pict_type;
    document.getElementById("fd-key").innerText = frame_map[frame_idx].key_frame === 0 ? "False" : "True";
    document.getElementById("fd-qp").innerText = frame_map[frame_idx].qp;
    document.getElementById("fd-pos").innerText = frame_map[frame_idx].pkt_pos;
    document.getElementById("fd-size").innerText = frame_map[frame_idx].pkt_size;
    document.getElementById("fd-interlaced").innerText = frame_map[frame_idx].interlaced_frame;
    document.getElementById("fd-top-field-first").innerText = frame_map[frame_idx].top_field_first;
    document.getElementById("fd-repeat-pict").innerText = frame_map[frame_idx].repeat_pict;
    document.getElementById("fd-chroma-location").innerText = frame_map[frame_idx].chroma_location;
    document.getElementById("fd-coded-pict-num").innerText = frame_map[frame_idx].coded_picture_number;
    document.getElementById("fd-dis-pict-num").innerText = frame_map[frame_idx].display_picture_number;
}


/**
 * Add event listener to video type selection
 * @type {HTMLElement}
 */
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


/**
 * Remove block overlay
 */
const remove_block_overlay = () => {
    let map = document.getElementById('block-overlay-map');
    map.innerHTML = "";
    // remove loading block data
    let children = document.getElementsByTagName("head")[0].children;
    for (let i = 0; i < children.length; i++) {
        if (children[i].src && children[i].src.includes('/report/files/blocks')) {
            children[i].remove();
        }
    }
}


/**
 * Load javascript file
 *
 * @param url js file path
 * @param callback function to be called when loading finished
 */
const load_script = (url, callback) => {
    let script = document.createElement("script")
    script.type = "text/javascript";

    if (script.readyState){  //IE
        script.onreadystatechange = function(){
            if (script.readyState === "loaded" ||
                    script.readyState === "complete"){
                script.onreadystatechange = null;
                callback();
            }
        };
    } else {  //Others
        script.onload = function(){
            callback();
        };
    }

    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
}


/**
 * Create block overlay for current frame
 */
const create_block_overlay = () => {
    let f_idx = get_cur_frame_idx("vis");
    let file_idx = Math.floor(f_idx / numFramePerFile);
    let file_name = "block_" + file_idx + ".js";
    load_script("./files/blocks/" + file_name, () => {
        let blocks = block_per_frame[f_idx % numFramePerFile];
        let map = document.getElementById('block-overlay-map');
        let w_ratio = 1280 / frame_map[0]['width'];
        let h_ratio = 720 / frame_map[0]['height'];
        for (let i = 0; i < blocks.length; i++) {
            let block = blocks[i];
            let x1 = parseInt(block[0]) * w_ratio;
            let y1 = parseInt(block[1]) * h_ratio;
            let x2 = x1 + parseInt(block[2]) * w_ratio;
            let y2 = y1 + parseInt(block[3]) * h_ratio;
            let area = document.createElement('area');
            area.href = "#";
            area.id = i;
            area.shape = "rect";
            area.coords = x1 + "," + y1 + "," + x2 + "," + y2;
            area.addEventListener("click", (e) => {
                let f_idx = get_cur_frame_idx("vis") % numFramePerFile;
                let block = block_per_frame[f_idx][e.target.id];
                document.getElementById('b-x').innerText = block[0];
                document.getElementById('b-y').innerText = block[1];
                document.getElementById('b-w').innerText = block[2];
                document.getElementById('b-h').innerText = block[3];
                document.getElementById('b-qp').innerText = parseInt(frame_map[f_idx]['qp']) + parseInt(frame_map[f_idx]['plane_delta_qp']) + block[4];
                document.getElementById('b-intra').innerText = block[5] === 0 ? "False" : "True";
                document.getElementById('b-skip').innerText = block[6] === 0 ? "False" : "True";
            });
            map.appendChild(area);
        }
        let basic_opts = {
            mapKey: 'id',
            singleSelect: true
        };
        let initial_opts = $.extend({},basic_opts,
            {
                staticState: true,
                fill: false,
                stroke: true,
                strokeWidth: 0.5,
                strokeColor: 'ff0000'
            });

        $('#overlay-img').mapster(initial_opts)
            .mapster('snapshot')
            .mapster('rebind',basic_opts);
    });
}


let bar = $("#bar");
let left = $("#left");
let right = $("#right");
let rightContent = $("#right-content");
let ssimVideos = $(".ssim-video");
let ssimVideoCurrentTime = 0;
let mouseDown = null;

const animateOverlap = () => {
    left.animate({
    'width': '640px'
    }, 10);

    right.animate({
    'width': '640px'
    }, 10);

    rightContent.animate({
    'margin-left': '-640px',
    }, 10);
}


/**
 * Sync the current time of main and ref videos
 */
const update_current_time_ssim = () => {
    Array.from(ssimVideos).forEach((video) => {
        video.currentTime = ssimVideoCurrentTime;
    });
}

const add_ssim_video_event_listener = () => {
    Array.from(ssimVideos).forEach((video) => {
        video.addEventListener("play", () => {
            Array.from(ssimVideos).forEach((video) => {
                video.play();
            });
        });
        video.addEventListener("pause", () => {
            Array.from(ssimVideos).forEach((video) => {
                video.pause();
            });
            ssimVideoCurrentTime = video.currentTime;
            // in case of playback delay
            update_current_time_ssim();
            // sync frame range slider
            let f_idx = get_cur_frame_idx("ssim");
            slider.value = f_idx;
            frameIdText.innerHTML = f_idx;
        });
        video.addEventListener("seeking", () => {
            if (video.currentTime === ssimVideoCurrentTime) return;
            ssimVideoCurrentTime = video.currentTime;
            update_current_time_ssim();
            let f_idx = get_cur_frame_idx("ssim");
            slider.value = f_idx;
            frameIdText.innerHTML = f_idx;
        });
    });
}
add_ssim_video_event_listener();

const mousemove = (event) => {
    if (!mouseDown) return false;
    let dx = event.clientX - mouseDown.clientX;
    left.width(left.width() + dx);
    right.width(right.width() - dx);
    rightContent.css('margin-left', -left.width() - bar.width());
    mouseDown = event;
};

const mouseup = (event) => {
    mouseDown = null;
}

bar.mousemove(mousemove);
left.mouseup(mouseup);
right.mouseup(mouseup);
left.mousemove(mousemove);
right.mousemove(mousemove);
bar.mousedown((event) => {
    mouseDown = event;
});
bar.mouseup(mouseup);

// Setup the transition to be overlapping.
setTimeout(animateOverlap, 1000);

// frame range slider
let slider = document.getElementById("frame-range-slider");
let frameIdText = document.getElementById("frame-id");
frameIdText.innerHTML = slider.value;

const init_slider = () => {
    slider.min = 0;
    slider.max = frame_ts.length - 1;

}
init_slider();

// Update the current slider value
slider.oninput = function() {
  frameIdText.innerHTML = this.value;
}
slider.onchange = function() {
    let f_idx = this.value;
    ssimVideoCurrentTime = Number(frame_ts[f_idx]) + offset;
    update_current_time_ssim();
}
