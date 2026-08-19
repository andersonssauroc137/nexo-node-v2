import { GAME_CONFIG } from "./config.js";


export class World {

    constructor(data) {

        this.width = data.width;
        this.height = data.height;

        this.spawn = {
            x: data.spawn.x,
            y: data.spawn.y,
        };

        this.backgroundColor = "#080b10";

        this.gridSize = 100;
    }


    update(deltaTime) {
        // Sistemas futuros do mundo.
    }


    render(context, camera) {

        context.fillStyle =
            this.backgroundColor;

        context.fillRect(
            0,
            0,
            GAME_CONFIG.canvas.width,
            GAME_CONFIG.canvas.height
        );


        this.renderGrid(
            context,
            camera
        );


        this.renderWorldBounds(
            context,
            camera
        );


        if (GAME_CONFIG.debug) {

            this.renderDebug(
                context,
                camera
            );
        }
    }


    renderGrid(context, camera) {

        const gridSize =
            this.gridSize;


        const startX =
            -(camera.x % gridSize);

        const startY =
            -(camera.y % gridSize);


        context.save();

        context.strokeStyle =
            "rgba(49, 230, 255, 0.08)";

        context.lineWidth = 1;


        for (
            let x = startX;
            x <= GAME_CONFIG.canvas.width;
            x += gridSize
        ) {

            context.beginPath();

            context.moveTo(
                x,
                0
            );

            context.lineTo(
                x,
                GAME_CONFIG.canvas.height
            );

            context.stroke();
        }


        for (
            let y = startY;
            y <= GAME_CONFIG.canvas.height;
            y += gridSize
        ) {

            context.beginPath();

            context.moveTo(
                0,
                y
            );

            context.lineTo(
                GAME_CONFIG.canvas.width,
                y
            );

            context.stroke();
        }


        context.restore();
    }


    renderWorldBounds(
        context,
        camera
    ) {

        const position =
            camera.worldToScreen(
                0,
                0
            );


        context.save();

        context.strokeStyle =
            "rgba(158, 108, 255, 0.5)";

        context.lineWidth = 4;


        context.strokeRect(
            position.x,
            position.y,
            this.width,
            this.height
        );


        context.restore();
    }


    renderDebug(
        context,
        camera
    ) {

        context.save();

        context.fillStyle =
            "rgba(49, 230, 255, 0.75)";

        context.font =
            "16px monospace";


        context.fillText(
            `WORLD ${this.width} x ${this.height}`,
            24,
            36
        );


        context.fillText(
            `CAMERA ${Math.round(camera.x)}, ${Math.round(camera.y)}`,
            24,
            62
        );


        context.restore();
    }
}