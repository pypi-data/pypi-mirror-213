import * as React from 'react';

import { voiceAtlasIcon, voiceAtlasWordmarkIcon } from '../style/IconsStyle';

interface IAboutDialog {
    aboutBody: JSX.Element;
    aboutTitle: JSX.Element
}

export function aboutVoiceAtlasDialog(): IAboutDialog {
    const versionInfo = (
        <span className="jp-About-version-info">
            <span className="jp-About-version">1.0</span>
        </span>
    );
    const aboutTitle = (
        <span className="jp-About-header">
            <voiceAtlasIcon.react margin="7px 9.5px" height="auto" width="58px" />
            <div className="jp-About-header-info">
                <voiceAtlasWordmarkIcon.react height="auto" width="196px" />
                {versionInfo}
            </div>
        </span>
    );

    const externalLinks = (
        <span className="jp-About-externalLinks">
            <a
                href='https://voiceatlas.com'
                target="_blank"
                rel="noopener noreferrer"
                className="jp-Button-flat"
            >
                {"About Voice Atlas"}
            </a>
        </span>
    );
    const copyright = (
        <span className="jp-About-copyright">
            {'© 2019-2022 Voice Atlas by Navteca LLC'}
        </span>
    );
    const aboutBody = (
        <div className="jp-About-body">
            {externalLinks}
            {copyright}
        </div>
    );

    return { aboutBody, aboutTitle }
}