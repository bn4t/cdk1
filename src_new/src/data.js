import {parse} from "@vanillaes/csv";

export class Data {

    pluvial_data = [];

    constructor() {
        this.pluvial_data = [];

        // fetch the csv file
        fetch('data/truncated.csv')
            .then(response => response.text())
            .then(data => {
                this.pluvial_data = parse(data, {header: true});
            });
    }


}