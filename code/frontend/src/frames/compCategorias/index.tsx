import styles from './styles.module.scss';
import Baby from '@myImages/baby.png';
import Bathroom from '@myImages/bathroom.png';
import Curtains from '@myImages/curtains.png';
import Room from '@myImages/room.png';


export default function CompCategorias() {
    return (
    <div className={styles.compCategorias}>
        <div className={styles.titleContainer}>
            <p>COMPRAR POR CATEGORIAS</p>
        </div>
        <div className={styles.categoriesContainer}>
            <div className={styles.category}>
                <figure>
                    <img src={Room} alt="category" loading="lazy" />
                </figure>
                <h2>Recamara</h2>
            </div>
            <div className={styles.category}>
                <figure>
                    <img src={Bathroom} alt="category" loading="lazy" />
                </figure>
                <h2>Baño</h2>
            </div>  
            <div className={styles.category}>
                <figure>
                    <img src={Baby} alt="category" loading="lazy" />
                </figure>
                <h2>Bebe</h2>
            </div>
            <div className={styles.category}>
                <figure>
                    <img src={Curtains} alt="category" loading="lazy" />
                </figure>
                <h2>Cortinas</h2>
            </div>
        </div>
    </div>
    );
}