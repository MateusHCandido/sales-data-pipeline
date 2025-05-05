from sales.cdc.kafka_producer import delivery_report  

def test_delivery_report_success(capfd):
    # Create a mock message simulating a successful delivery
    class MockMsg:
        def topic(self): return 'sales-cdc'
        def partition(self): return 0

    # Call the delivery report with no error
    delivery_report(None, MockMsg())

    # Check if the success message was printed correctly
    out, _ = capfd.readouterr()
    expected = "Mensagem entregue em sales-cdc [0]"
    assert expected in out, f"Expected: '{expected}' | Got: '{out.strip()}'"


def test_delivery_report_error(capfd):
    # Call the delivery report with a simulated error
    delivery_report("Erro simulado", None)

    # Check if the error message was printed correctly
    out, _ = capfd.readouterr()
    expected = "Erro ao entregar mensagem: Erro simulado"
    assert expected in out, f"Expected: '{expected}' | Got: '{out.strip()}'"


