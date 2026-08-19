import { GAME_CONFIG } from "../core/config.js";


const SHIRT_COLORS = {
    cyan: "#31e6ff",
    purple: "#9e6cff",
    green: "#55e39f",
    red: "#ff657a",
    yellow: "#ffd76a",
    white: "#e8edf2",
};


export class Player {

    constructor({
        x,
        y,
        operator,
    }) {

        this.x = x;
        this.y = y;

        this.width =
            GAME_CONFIG.player.width;

        this.height =
            GAME_CONFIG.player.height;

        this.speed =
            GAME_CONFIG.player.speed;


        this.presentation =
            operator.presentation;

        this.shirtColor =
            operator.shirt_color;


        this.direction = "down";

        this.isMoving = false;
    }


    update(
        deltaTime,
        input,
        world
    ) {

        const movement =
            input.getMovementVector();


        let directionX =
            movement.x;

        let directionY =
            movement.y;


        const length =
            Math.hypot(
                directionX,
                directionY
            );


        if (length > 0) {

            directionX /= length;
            directionY /= length;

            this.isMoving = true;


            this.updateDirection(
                directionX,
                directionY
            );

        } else {

            this.isMoving = false;
        }


        const nextX =
            this.x
            + directionX
            * this.speed
            * deltaTime;


        const nextY =
            this.y
            + directionY
            * this.speed
            * deltaTime;


        this.x =
            this.clamp(
                nextX,
                this.width / 2,
                world.width
                    - this.width / 2
            );


        this.y =
            this.clamp(
                nextY,
                this.height / 2,
                world.height
                    - this.height / 2
            );
    }


    updateDirection(
        directionX,
        directionY
    ) {

        if (
            Math.abs(directionX)
            > Math.abs(directionY)
        ) {

            this.direction =
                directionX > 0
                    ? "right"
                    : "left";

        } else {

            this.direction =
                directionY > 0
                    ? "down"
                    : "up";
        }
    }


    clamp(
        value,
        minimum,
        maximum
    ) {

        return Math.max(
            minimum,
            Math.min(
                value,
                maximum
            )
        );
    }


    render(
        context,
        camera
    ) {

        const screen =
            camera.worldToScreen(
                this.x,
                this.y
            );


        const shirtColor =
            SHIRT_COLORS[
                this.shirtColor
            ]
            || "#31e6ff";


        context.save();


        this.renderShadow(
            context,
            screen
        );


        this.renderBody(
            context,
            screen,
            shirtColor
        );


        context.restore();
    }


    renderShadow(
        context,
        screen
    ) {

        context.fillStyle =
            "rgba(0, 0, 0, 0.45)";


        context.beginPath();

        context.ellipse(
            screen.x,
            screen.y + 22,
            17,
            7,
            0,
            0,
            Math.PI * 2
        );

        context.fill();
    }


    renderBody(
        context,
        screen,
        shirtColor
    ) {

        /*
         * Cabeça
         */

        context.fillStyle =
            "#d9aa82";

        context.fillRect(
            screen.x - 7,
            screen.y - 24,
            14,
            13
        );


        /*
         * Cabelo
         */

        context.fillStyle =
            "#141414";

        context.fillRect(
            screen.x - 8,
            screen.y - 26,
            16,
            5
        );


        /*
         * Camiseta
         */

        context.fillStyle =
            shirtColor;

        context.fillRect(
            screen.x - 10,
            screen.y - 11,
            20,
            21
        );


        /*
         * Calça
         */

        context.fillStyle =
            "#252b33";

        context.fillRect(
            screen.x - 9,
            screen.y + 10,
            7,
            13
        );

        context.fillRect(
            screen.x + 2,
            screen.y + 10,
            7,
            13
        );


        /*
         * Indicador inferior
         */

        context.strokeStyle =
            "rgba(49, 230, 255, 0.7)";

        context.lineWidth = 2;


        context.beginPath();

        context.arc(
            screen.x,
            screen.y + 24,
            19,
            0,
            Math.PI * 2
        );

        context.stroke();
    }
}