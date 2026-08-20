export class Building {

    constructor(data) {

        this.id = data.id;

        this.name = data.name;
        this.slug = data.slug;

        this.imageUrl =
            data.image;


        this.x = data.x;
        this.y = data.y;

        this.width =
            data.width;

        this.height =
            data.height;


        this.collision = {
            x:
                data.collision.x,

            y:
                data.collision.y,

            width:
                data.collision.width,

            height:
                data.collision.height,
        };

        this.interaction = {
            enabled:
                data.interaction?.enabled
                ?? false,

            x:
                data.interaction?.x
                ?? 0,

            y:
                data.interaction?.y
                ?? 0,

            width:
                data.interaction?.width
                ?? 0,

            height:
                data.interaction?.height
                ?? 0,

            type:
                data.interaction?.type
                ?? null,
        };


        this.image = new Image();

        this.isLoaded = false;

        this.hasImageError = false;
    }


    load() {

        return new Promise(
            resolve => {

                this.image.onload =
                    () => {

                        this.isLoaded =
                            true;

                        resolve();
                    };


                this.image.onerror =
                    () => {

                        this.hasImageError =
                            true;

                        console.error(
                            `Building image failed: ${this.imageUrl}`
                        );

                        resolve();
                    };


                this.image.src =
                    this.imageUrl;
            }
        );
    }


    get sortY() {

        return (
            this.y
            + this.height
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


        if (this.isLoaded) {

            context.drawImage(
                this.image,

                screen.x,
                screen.y,

                this.width,
                this.height
            );

            return;
        }


        this.renderFallback(
            context,
            screen
        );
    }


    renderFallback(
        context,
        screen
    ) {

        context.save();


        context.fillStyle =
            "rgba(158, 108, 255, 0.15)";


        context.strokeStyle =
            "#9e6cff";


        context.fillRect(
            screen.x,
            screen.y,
            this.width,
            this.height
        );


        context.strokeRect(
            screen.x,
            screen.y,
            this.width,
            this.height
        );


        context.fillStyle =
            "#9e6cff";


        context.font =
            "16px monospace";


        context.fillText(
            this.name,
            screen.x + 12,
            screen.y + 24
        );


        context.restore();
    }
}