import styles from './styles.module.scss';


interface Props {
    text: string;
}


export default function Button(props: Props) {
    return (
        <button className={styles.button}>
            <span className={styles.placeholder}>{props.text}</span>
            <span className={styles.firstText}>{props.text}</span>
            <span className={styles.secondText}>{props.text}</span>
        </button>
    );
}