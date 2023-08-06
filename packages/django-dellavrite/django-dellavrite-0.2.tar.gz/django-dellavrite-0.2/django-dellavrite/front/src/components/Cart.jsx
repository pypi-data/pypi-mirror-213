import React, {useEffect, useState} from 'react';
import {Instance} from "../http/Instance";
import {Link, useNavigate} from "react-router-dom";

const Cart = ({setTitle, token}) => {

    const [items, setItems] = useState([])

    const navigate = useNavigate()

    const sorting = (arr) => {
        const result = [];
        arr.forEach(item => {
            item.count = 1;
            const found = result.find(elem => elem.product_id === item.product_id);
            found ? found.count++ : result.push(item)
        });
        return result
    }

    const getCart = () => {
        Instance('cart', 'GET', token).then(rez => rez.json().then(data =>
            setItems(sorting(data.data))))
    }

    const increment = (index) => {
        const copy = [...items]
        copy[index].count += 1
        setItems(copy)
    }


    const deleteFromCart = async (id) => {
        await Instance(`cart/${id}`, 'DELETE', token);
        setItems(items.filter(item => item.id !== id));
    };

    const decrement = (index) => {
        const copy = [...items];
        copy[index].count -= 1;
        setItems(copy);
    };

    useEffect(() => {
        setTitle('Корзина');
        getCart();
    }, []);

    const makeOrder = async () => {
        await Instance('order', 'POST', token)
        navigate('/orders')
    }

    const total_cost = items && items.reduce((a, item) => a += item.price * item.count, 0)


    return (
        <main>
            <div className="row row-cols-1 row-cols-md-3 mb-3 text-center">
                {

                    items.map((item, i) =>
                        <div className="col" key={item.id}>
                            <div className="card mb-4 rounded-3 shadow-sm">
                                <div className="card-header py-3">
                                    <h4 className="my-0 fw-normal">{item.name}</h4>
                                </div>
                                <div className="card-body">
                                    <h1 className="card-title pricing-card-title">{item.price}р.<small
                                        className="text-muted fw-light"> &times; {item.count}
                                        шт.</small></h1>
                                    <p>{item.description}</p>

                                    <button onClick={e => increment(i)} type="button"
                                            className="btn btn-lg btn-info mb-3">+
                                    </button>
                                    <button onClick={e => decrement(i)} type="button"
                                            className="btn btn-lg btn-warning mb-3">&minus;</button>
                                    <button onClick={() => deleteFromCart(item.id)} type="button"
                                            className="btn btn-lg btn-outline-danger mb-3">Удалить из
                                        корзины
                                    </button>
                                </div>
                            </div>
                        </div>
                    )

                }
            </div>
            <div className="row justify-content-center gap-1">
                {
                    items && items.length !== 0 &&
                    <h2 className="mb-5">Итоговая стоимость: {total_cost}р.</h2>

                }

                <Link to={'/'} className="col-6 btn btn-lg btn-outline-secondary mb-3" type="button">Назад</Link>
                {
                    items && items.length !== 0 &&
                    <button onClick={() => makeOrder()} type="button"
                            className="col-6 btn btn-lg btn-success mb-3">Оформить заказ</button>
                }

            </div>
        </main>
    );
};

export default Cart;