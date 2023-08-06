
export default class AppChatlas extends HTMLElement {
    constructor(notebookName: string, atlasId: string) {
        super();
        var chatlas = Object.create(HTMLElement.prototype);

        chatlas.createdCallback = function () {

            var shadow = this.createShadowRoot();
            const script = document.createElement('script')
            script.setAttribute("src", "https://bot.dev.voiceatlas.com/v1/chatlas.js")
            script.setAttribute("async", "")
            shadow.appendChild(script)

            // Verify if custom element already exists
            // if exists change attribute
            // else define it
            const chatlas = document.createElement('app-chatlas')
            chatlas.setAttribute('name', notebookName)
            chatlas.setAttribute('id', notebookName)
            chatlas.setAttribute("atlas-id", atlasId)
            chatlas.setAttribute("full-screen", "true")
            chatlas.setAttribute("voice-enabled", "true")
            shadow.appendChild(chatlas)

        };

        // var xChatlas = document.createElement("app-chatlas", {
        //     prototype: chatlas
        // });
        customElements.define('app-chatlas', chatlas)
        return chatlas
        // const script = document.createElement('script')
        // script.setAttribute("src", "https://bot.dev.voiceatlas.com/v1/chatlas.js")
        // script.setAttribute("async", "")
        // document.body.appendChild(script)

        // // Verify if custom element already exists
        // // if exists change attribute
        // // else define it
        // const chatlas = document.createElement('app-chatlas')
        // chatlas.setAttribute('name', notebookName)
        // chatlas.setAttribute('id', notebookName)
        // chatlas.setAttribute("atlas-id", atlasId)
        // chatlas.setAttribute("full-screen", "true")
        // chatlas.setAttribute("widget-background-color", "#3f51b5ff")
        // chatlas.setAttribute("widget-text-color", "#ffffffff")
        // chatlas.setAttribute("widget-title", "Chatlas")
        // document.body.appendChild(chatlas)
        // return chatlas;
    }
}