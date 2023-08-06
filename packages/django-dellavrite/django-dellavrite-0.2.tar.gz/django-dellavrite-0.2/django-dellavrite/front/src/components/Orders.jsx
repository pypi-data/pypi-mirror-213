import React, {useEffect, useState} from 'react';
import {Link} from "react-router-dom";
import {Instance} from "../http/Instance";
import login from "./Login";

const Orders = ({setTitle, token}) => {

    const [products, setProducts] = useState([])
    const [items, setItems] = useState([])

    const getOrders = async () => {
        await Instance('products', 'GET').then(res => res.json()).then(data => setProducts(data.data))
        await Instance('order', 'GET', token).then(res => res.json()).then(data => setItems(data.data))

    }

    useEffect(() => {
        setTitle('Ваши заказы')
        getOrders()
    }, [])

    return (
        <main>
            {
                items.map(item =>
                    <div className="row row-cols-1 row-cols-md-3 mb-3 text-center bg-light" key={item.id}>
                        <h2 className="w-100">Заказ №{item.id}</h2>

                        {
                            item.products.map((product_id, index) => {
                                const product = products.find(item => item.id === product_id)

                                return (
                                    <div className="col" key={index}>
                                        <div className="card mb-4 rounded-3 shadow-sm">
                                            <div className="card-header py-3">
                                                <h4 className="my-0 fw-normal">{product.name}</h4>
                                            </div>
                                            <div className="card-body">
                                                <h1 className="card-title pricing-card-title">{product.price}р.<small
                                                    className="text-muted fw-light"> &times; шт.</small></h1>
                                                <p>{product.description}</p>
                                            </div>
                                        </div>
                                    </div>
                                )
                            })
                        }
                        <h2 className="w-100">Итоговая стоимость: {item.order_price}р.</h2>
                    </div>
                )
            }

            <div className="row justify-content-center gap-1">
                <Link to={'/'} className="col-6 btn btn-lg btn-outline-secondary mb-3" type="button">Назад</Link>
            </div>
        </main>
    );
};

export default Orders;