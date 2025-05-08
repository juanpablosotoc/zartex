import Button from '@myComponents/button';
import styles from './styles.module.scss';


interface Props {
    img: string;
}

export default function Conocenos(props: Props) {
    return (
        <div className={styles.wrapper}>
            <img src={props.img} alt="conocenos" />
            <div className={styles.content}>
                <p className={styles.title}>Donde la Excelencia se encuentra con la Innovación</p>
                <Button text='Conocenos' />
            </div>
        </div>
    )
}