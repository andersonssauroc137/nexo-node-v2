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


async start() {

    this.canvas.width =
        GAME_CONFIG.canvas.width;

    this.canvas.height =
        GAME_CONFIG.canvas.height;


    this.context.imageSmoothingEnabled =
        false;


    this.renderLoading();


    await this.world.loadAssets();


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


    const renderables = [
        ...this.world.buildings,
        this.player,
    ];


    renderables.sort(
        (
            first,
            second
        ) =>
            first.sortY
            - second.sortY
    );


    for (
        const entity
        of renderables
    ) {

        entity.render(
            this.context,
            this.camera
        );
    }


    if (GAME_CONFIG.debug) {

        this.renderCollisionDebug();

        this.renderDebug();
    }
}


renderLoading() {

    const context =
        this.context;


    context.fillStyle =
        "#080b10";


    context.fillRect(
        0,
        0,
        this.canvas.width,
        this.canvas.height
    );


    context.fillStyle =
        "#31e6ff";


    context.font =
        "22px monospace";


    context.textAlign =
        "center";


    context.fillText(
        "SINCRONIZANDO FORTALEZA NODE...",
        this.canvas.width / 2,
        this.canvas.height / 2
    );


    context.textAlign =
        "left";
}

renderCollisionDebug() {

    const context =
        this.context;


    context.save();


    /*
     * Buildings
     */

    context.strokeStyle =
        "rgba(255, 101, 122, 0.9)";

    context.fillStyle =
        "rgba(255, 101, 122, 0.12)";

    context.lineWidth = 2;


    for (
        const building
        of this.world.buildings
    ) {

        const screen =
            this.camera.worldToScreen(
                building.collision.x,
                building.collision.y
            );


        context.fillRect(
            screen.x,
            screen.y,
            building.collision.width,
            building.collision.height
        );


        context.strokeRect(
            screen.x,
            screen.y,
            building.collision.width,
            building.collision.height
        );
    }


    /*
     * Player
     */

    const playerBox =
        this.player
            .getCollisionBoxAt(
                this.player.x,
                this.player.y
            );


    const playerScreen =
        this.camera.worldToScreen(
            playerBox.x,
            playerBox.y
        );


    context.strokeStyle =
        "#31e6ff";

    context.fillStyle =
        "rgba(49, 230, 255, 0.18)";


    context.fillRect(
        playerScreen.x,
        playerScreen.y,
        playerBox.width,
        playerBox.height
    );


    context.strokeRect(
        playerScreen.x,
        playerScreen.y,
        playerBox.width,
        playerBox.height
    );


    context.restore();
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
            `BUILDINGS ${this.world.buildings.length}`,
            24,
            168
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