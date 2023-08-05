const css = `
table.panel-df {
    margin-left: auto;
    margin-right: auto;
    border: none;
    border-collapse: collapse;
    border-spacing: 0;
    color: black;
    font-size: 12px;
    table-layout: fixed;
    width: 100%;
}

.panel-df tr, .panel-df th, .panel-df td {
    text-align: right;
    vertical-align: middle;
    padding: 0.5em 0.5em !important;
    line-height: normal;
    white-space: normal;
    max-width: none;
    border: none;
}

.panel-df tbody {
    display: table-row-group;
    vertical-align: middle;
    border-color: inherit;
}

.panel-df tbody tr:nth-child(odd) {
    background: #f5f5f5;
}

.panel-df thead {
    border-bottom: 1px solid black;
    vertical-align: bottom;
}

.panel-df tr:hover {
    background: lightblue !important;
    cursor: pointer;
}
`;
export default css;
