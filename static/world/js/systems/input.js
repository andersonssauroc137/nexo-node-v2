export class Input {

    constructor() {

        this.keys = new Set();

        this.handleBlur =
            this.handleBlur.bind(this);


        this.handleKeyDown =
            this.handleKeyDown.bind(this);

        this.handleKeyUp =
            this.handleKeyUp.bind(this);


        window.addEventListener(
            "keydown",
            this.handleKeyDown
        );

        window.addEventListener(
            "blur",
            this.handleBlur
        );


        window.addEventListener(
            "keyup",
            this.handleKeyUp
        );

        this.pressedOnce =
            new Set();

        
    }

    handleBlur() {

        this.keys.clear();
        this.pressedOnce.clear();
    }


    handleKeyDown(event) {

        const key =
            event.key.toLowerCase();


        if (
            [
                "w",
                "a",
                "s",
                "d",
                "arrowup",
                "arrowdown",
                "arrowleft",
                "arrowright",
                "e",
            ].includes(key)
        ) {

            event.preventDefault();
        }


        this.keys.add(key);
    }

    wasPressed(key) {

        const normalized =
            key.toLowerCase();


        if (
            this.pressedOnce.has(
                normalized
            )
        ) {

            this.pressedOnce.delete(
                normalized
            );

            return true;
        }


        return false;
    }


    handleKeyUp(event) {

        this.keys.delete(
            event.key.toLowerCase()
        );
    }


    isPressed(...keys) {

        return keys.some(
            key =>
                this.keys.has(
                    key.toLowerCase()
                )
        );
    }


    getMovementVector() {

        let x = 0;
        let y = 0;


        if (
            this.isPressed(
                "a",
                "arrowleft"
            )
        ) {
            x -= 1;
        }


        if (
            this.isPressed(
                "d",
                "arrowright"
            )
        ) {
            x += 1;
        }


        if (
            this.isPressed(
                "w",
                "arrowup"
            )
        ) {
            y -= 1;
        }


        if (
            this.isPressed(
                "s",
                "arrowdown"
            )
        ) {
            y += 1;
        }


        return {
            x,
            y,
        };
    }
}