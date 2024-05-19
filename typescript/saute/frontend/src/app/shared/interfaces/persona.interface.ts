export interface Persona {
    icon: string;
    iconPath: string;
    title: string;
    task: string;
    bio: string[];
    systemPrompt: string;
    capBg: { [key: string]: string };
    buttonLink: string;
    name: string;
    iceBreakers: Array<string>;
    hashtags: Array<string>;
}
