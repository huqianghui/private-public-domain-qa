import { Example } from "./Example";

import styles from "./Example.module.css";

export type ExampleModel = {
    text: string;
    value: string;
};

const EXAMPLES: ExampleModel[] = [
    {
        text: "2022-23赛季，NBA哪只球队常规赛战绩最好?",
        value: "2022-23赛季，NBA哪只球队常规赛战绩最好?"
    },
    { text: "What's the main goal of gpt model ?", value: "What's the main goal of gpt model ?" },
    { text: "涨幅最高的三只股票是？", value: "查询出涨幅最高的三只股票" }
];

interface Props {
    onExampleClicked: (value: string) => void;
}

export const ExampleList = ({ onExampleClicked }: Props) => {
    return (
        <ul className={styles.examplesNavList}>
            {EXAMPLES.map((x, i) => (
                <li key={i}>
                    <Example text={x.text} value={x.value} onClick={onExampleClicked} />
                </li>
            ))}
        </ul>
    );
};
