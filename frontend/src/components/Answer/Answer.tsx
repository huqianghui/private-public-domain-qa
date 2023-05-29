import { useMemo } from "react";
import { Stack, IconButton } from "@fluentui/react";
import DOMPurify from "dompurify";

import styles from "./Answer.module.css";

import { AskResponse, getCitationFilePath } from "../../api";
import { parseAnswerToHtml } from "./AnswerParser";
import { parseArrayAnswerToHtml } from "./ArrayAnswerParser";
import { AnswerIcon } from "./AnswerIcon";

interface Props {
    answer: AskResponse;
    isSelected?: boolean;
    onCitationClicked: (filePath: string) => void;
    onThoughtProcessClicked: () => void;
    onSupportingContentClicked: () => void;
    onFollowupQuestionClicked?: (question: string) => void;
    onReadAnswerClicked: () => void;
    showFollowupQuestions?: boolean;
}

export const Answer = ({
    answer,
    isSelected,
    onCitationClicked,
    onThoughtProcessClicked,
    onSupportingContentClicked,
    onFollowupQuestionClicked,
    onReadAnswerClicked,
    showFollowupQuestions
}: Props) => {
    if(typeof answer.answer === "string"){
    const parsedAnswer = useMemo(() => parseAnswerToHtml(answer.answer, onCitationClicked), [answer]);
    const sanitizedAnswerHtml = DOMPurify.sanitize(parsedAnswer.answerHtml);

    return (
        <Stack className={`${styles.answerContainer} ${isSelected && styles.selected}`} verticalAlign="space-between">
            <Stack.Item>
                <Stack horizontal horizontalAlign="space-between">
                    <AnswerIcon />
                    <div>
                        <IconButton
                            style={{ color: "black" }}
                            iconProps={{ iconName: "Lightbulb" }}
                            title="Show thought process"
                            ariaLabel="Show thought process"
                            onClick={() => onThoughtProcessClicked()}
                            disabled={!answer.thoughts}
                        />
                        <IconButton
                            style={{ color: "black" }}
                            iconProps={{ iconName: "ClipboardList" }}
                            title="Show supporting content"
                            ariaLabel="Show supporting content"
                            onClick={() => onSupportingContentClicked()}
                            disabled={!answer.data_points.length}
                        />
                        <IconButton
                            style={{color: "black"}}
                            iconProps={{ iconName: "ReadOutLoud"}}
                            title="Read answer"
                            ariaLabel="Read answer"
                            onClick={() => onReadAnswerClicked()}
                            disabled= {!answer.answer}
                        />
                    </div>
                </Stack>
            </Stack.Item>

            <Stack.Item grow>
                <div className={styles.answerText} dangerouslySetInnerHTML={{ __html: sanitizedAnswerHtml }}></div>
            </Stack.Item>

            {!!parsedAnswer.citations.length && (
                <Stack.Item>
                    <Stack horizontal wrap tokens={{ childrenGap: 5 }}>
                        <span className={styles.citationLearnMore}>来源:</span>
                        {parsedAnswer.citations.map((x, i) => {
                            // const path = getCitationFilePath(x);
                            const path = x.path;
                            return (
                                <a key={i} className={styles.citation} title={x.name} onClick={() => onCitationClicked(path)}>
                                    {`${++i}. ${x.name}`}
                                </a>
                            );
                        })}
                    </Stack>
                </Stack.Item>
            )}

            {!!parsedAnswer.followupQuestions.length && showFollowupQuestions && onFollowupQuestionClicked && (
                <Stack.Item>
                    <Stack horizontal wrap className={`${!!parsedAnswer.citations.length ? styles.followupQuestionsList : ""}`} tokens={{ childrenGap: 6 }}>
                        <span className={styles.followupQuestionLearnMore}>您可能还想问:</span>
                        {parsedAnswer.followupQuestions.map((x, i) => {
                            return (
                                <a key={i} className={styles.followupQuestion} title={x} onClick={() => onFollowupQuestionClicked(x)}>
                                    {`${x}`}
                                </a>
                            );
                        })}
                    </Stack>
                </Stack.Item>
            )}
        </Stack>
    );
                    }else if(Array.isArray(answer.answer)){
                        let arrayAnswer:Array<string> = answer.answer;
                        const parsedAnswer = useMemo(() => parseArrayAnswerToHtml(arrayAnswer), [answer]);
                        const sanitizedAnswerHtml = DOMPurify.sanitize(parsedAnswer);
                    
                        return (
                            <Stack className={`${styles.answerContainer} ${isSelected && styles.selected}`} verticalAlign="space-between">
                                <Stack.Item>
                                    <Stack horizontal horizontalAlign="space-between">
                                        <AnswerIcon />
                                        <div>
                                            <IconButton
                                                style={{ color: "black" }}
                                                iconProps={{ iconName: "Lightbulb" }}
                                                title="Show thought process"
                                                ariaLabel="Show thought process"
                                                onClick={() => onThoughtProcessClicked()}
                                                disabled={!answer.thoughts}
                                            />
                                            <IconButton
                                                style={{ color: "black" }}
                                                iconProps={{ iconName: "ClipboardList" }}
                                                title="Show supporting content"
                                                ariaLabel="Show supporting content"
                                                onClick={() => onSupportingContentClicked()}
                                                disabled={!answer.data_points.length}
                                            />
                                            <IconButton
                                                style={{color: "black"}}
                                                iconProps={{ iconName: "ReadOutLoud"}}
                                                title="Read answer"
                                                ariaLabel="Read answer"
                                                onClick={() => onReadAnswerClicked()}
                                                disabled= {!answer.answer}
                                            />
                                        </div>
                                    </Stack>
                                </Stack.Item>
                    
                                <Stack.Item grow>
                                    <div className={styles.answerText} dangerouslySetInnerHTML={{ __html: sanitizedAnswerHtml }}></div>
                                </Stack.Item>
                            </Stack>
                        );
                    }else{
                        return null;
                    }
};
