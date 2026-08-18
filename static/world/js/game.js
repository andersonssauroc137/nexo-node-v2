import { GAME_CONFIG } from "./core/config.js";
import { World } from "./core/world.js";
import { Camera } from "./core/camera.js";


class Game {

    constructor(canvas) {

        this.canvas = canvas;

        this.context =
            canvas.getContext("2d");

        this.world = new World();
        this.camera = new Camera();

        this.camera.setPosition(
            600,
            400
        );

        this.lastTimestamp = 0;

        this.running = false;

        this.fpsElement =
            document.querySelector(
                "[data-game-fps]"
            );
    }


    start() {

        this.canvas.width =
            GAME_CONFIG.canvas.width;

        this.canvas.height =
            GAME_CONFIG.canvas.height;


        this.context.imageSmoothingEnabled =
            false;


        this.running = true;

        requestAnimationFrame(
            this.loop.bind(this)
        );
    }


    loop(timestamp) {

        if (!this.running) {
            return;
        }


        const deltaTime =
            Math.min(
                (
                    timestamp
                    - this.lastTimestamp
                ) / 1000,
                0.1
            );


        this.lastTimestamp = timestamp;


        this.update(deltaTime);

        this.render();


        this.updateDebugInfo(
            deltaTime
        );


        requestAnimationFrame(
            this.loop.bind(this)
        );
    }


    update(deltaTime) {

        this.world.update(
            deltaTime
        );
    }


    render() {

        this.world.render(
            this.context,
            this.camera
        );
    }


    updateDebugInfo(deltaTime) {

        if (
            !this.fpsElement
            || deltaTime <= 0
        ) {
            return;
        }


        const fps =
            Math.round(
                1 / deltaTime
            );


        this.fpsElement.textContent =
            String(fps);
    }
}

function loadOperatorData() {

    const element =
        document.getElementById(
            "game-operator-data"
        );


    if (!element) {

        throw new Error(
            "Operator data not found."
        );
    }


    return JSON.parse(
        element.textContent
    );
}

function loadJsonData(elementId) {

    const element =
        document.getElementById(
            elementId
        );


    if (!element) {

        throw new Error(
            `Game data not found: ${elementId}`
        );
    }


    return JSON.parse(
        element.textContent
    );
}


const canvas =
    document.getElementById(
        "game-canvas"
    );


if (canvas) {

    const operator =
        loadJsonData(
            "game-operator-data"
        );


    const worldData =
        loadJsonData(
            "game-world-data"
        );


    console.log(
        "NEXO NODE // OPERATOR",
        operator
    );


    console.log(
        "NEXO NODE // WORLD",
        worldData
    );


    const game =
        new Game(canvas);

    game.start();
}