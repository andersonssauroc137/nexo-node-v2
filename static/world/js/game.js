import { GAME_CONFIG } from "./core/config.js";
import { World } from "./core/world.js";
import { Camera } from "./core/camera.js";

import { Player } from "./entities/player.js";

import { Input } from "./systems/input.js";


class Game {

    constructor({
        canvas,
        operator,
        worldData,
    }) {

        this.canvas = canvas;

        this.context =
            canvas.getContext("2d");


        this.operator =
            operator;


        this.world =
            new World(
                worldData
            );


        this.input =
            new Input();


        this.player =
            new Player({
                x: this.world.spawn.x,
                y: this.world.spawn.y,
                operator:
                    this.operator,
            });


        this.camera =
            new Camera();


        this.camera.follow(
            this.player,
            this.world
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
            this.lastTimestamp
                ? Math.min(
                    (
                        timestamp
                        - this.lastTimestamp
                    ) / 1000,
                    0.1
                )
                : 0;


        this.lastTimestamp =
            timestamp;


        this.update(
            deltaTime
        );


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


        this.player.update(
            deltaTime,
            this.input,
            this.world
        );


        this.camera.follow(
            this.player,
            this.world
        );
    }


    render() {

        this.world.render(
            this.context,
            this.camera
        );


        this.player.render(
            this.context,
            this.camera
        );


        if (GAME_CONFIG.debug) {

            this.renderDebug();
        }
    }


    renderDebug() {

        const context =
            this.context;


        context.save();


        context.fillStyle =
            "rgba(255, 255, 255, 0.8)";

        context.font =
            "15px monospace";


        context.fillText(
            `PLAYER ${Math.round(this.player.x)}, ${Math.round(this.player.y)}`,
            24,
            90
        );


        context.fillText(
            `DIR ${this.player.direction}`,
            24,
            116
        );


        context.fillText(
            this.player.isMoving
                ? "STATE WALK"
                : "STATE IDLE",
            24,
            142
        );


        context.restore();
    }


    updateDebugInfo(
        deltaTime
    ) {

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


function loadJsonData(
    elementId
) {

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
        new Game({
            canvas,
            operator,
            worldData,
        });


    game.start();
}