import styles from './styles.module.scss';


interface Props {
    imgs: {
        img: string;
        alt: string;
    }[];
}


export default function NuevProd(props: Props) {
    return (
        <div className={styles.wrapper}>
            <p className={styles.title}>Nuevos Productos</p>
            <p className={styles.description}>Diseñados para quienes buscan experiencias que acarician tus sentidos.</p>
            <div className={styles.newProducts}>
                {props.imgs.map((img, index) => (
                    <div className={styles.newProduct} key={`${img.alt}-${index}`}>
                        <img src={img.img} alt={img.alt} />
                    </div>
                ))}
            </div>
        </div>
    )
}