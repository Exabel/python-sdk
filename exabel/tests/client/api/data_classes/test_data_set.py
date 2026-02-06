from exabel.client.api.data_classes.data_set import DataSet


class TestDataSet:
    def test_proto_conversion(self):
        data_set = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig1", "signals/ns.sig2"],
        )
        assert data_set == DataSet.from_proto(data_set.to_proto())

    def test_constructor_without_signals(self):
        data_set = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
        )
        assert [] == data_set.signals

    def test_equals(self):
        data_set_1 = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig1", "signals/ns.sig2"],
            derived_signals=["derivedSignals/123", "derivedSignals/321"],
            highlighted_signals=["derivedSignals/123", "derivedSignals/321"],
        )
        data_set_2 = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig2", "signals/ns.sig1"],
            derived_signals=["derivedSignals/123", "derivedSignals/321"],
            highlighted_signals=["derivedSignals/321", "derivedSignals/123"],
        )
        data_set_3 = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig2"],
        )
        data_set_4 = DataSet(
            name="dataSet/customerA.MyData",
            display_name="Revenue per store.",
            description="description",
            signals=["signals/ns.sig2", "signals/ns.sig1"],
            derived_signals=["derivedSignals/321", "derivedSignals/123"],
            highlighted_signals=["derivedSignals/123", "derivedSignals/321"],
        )
        assert data_set_1 == data_set_2
        assert data_set_1 != data_set_3
        assert data_set_1 != data_set_4
