import { parseSupportingContentItem } from "./SupportingContentParser";

import styles from "./SupportingContent.module.css";

interface Props {
    supportingContent: string[];
}

export const SupportingContent = ({ supportingContent }: Props) => {
    if(Array.isArray(supportingContent)){
        return (
            <ul className={styles.supportingContentNavList}>
                {supportingContent.map((x, i) => {
                    const parsed = parseSupportingContentItem(x);
    
                    return (
                        <li className={styles.supportingContentItem}>
                            <h4 className={styles.supportingContentItemHeader}>{parsed.title}</h4>
                            <p className={styles.supportingContentItemText}>{parsed.content}</p>
                            <a className={styles.supportingContentItemText} href={parsed.url} target="_blank">{parsed.url}</a>
                        </li>
                    );
                })}
            </ul>
        );
    }else if(typeof supportingContent === "string"){
        return (
            <ul className={styles.supportingContentNavList}>
                <li className={styles.supportingContentItem}>
                    <p className={styles.supportingContentItemText}>{supportingContent}</p>
                </li>
            </ul>
        );
    }else{
        return (<ul></ul>)
    }

    
};
