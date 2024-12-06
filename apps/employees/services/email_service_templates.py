def generate_email_templates(instance):
    formatted_start_date = instance.start_date.strftime("%d/%m/%Y") if instance.start_date else None

    TEMPLATES = {
        "email_body_intro": {
            "Opened": f"<p>Foi criada a requisição Nº {instance.control_number} de funcionário por {instance.requester}</p>",  # noqa: E501
            "Pending": f"<p>A requisição Nº {instance.control_number} de funcionário foi aprovada por {instance.approver} e agora está pendente.</p>",
            "Approved": f"<p>A requisição Nº {instance.control_number} de funcionário foi finalizada. O processo pode seguir. Favor, cada setor, tomar as seguintes providências:</p>",  # noqa: E501
            "Denied": f"<p>A requisição Nº {instance.control_number} de funcionário foi negada por {instance.approver}. Motivo: {instance.motive_denied}</p>",
        },
        "summary_body": f"""
            <h2>Dados da solicitação:</h2>
            Número de controle: {instance.control_number}<br>
            Empresa: {instance.company}<br>
            Departamento: {instance.cost_center.name}<br>
            Cargo: {instance.position.position}<br>
            Data solicitada: {instance.request_date.strftime("%d/%m/%Y")}<br>
            Motivo: {instance.motive}<br>
            Requisitante: {instance.requester}<br>
            Aprovador: {instance.approver}<br>
            Observações: {instance.obs}<br>
        """,
        "RH": {
            "Pending": """
                <h3>RH ⬇️</h3>
                <ul>
                    <li>Abrir a vaga para o candidato selecionado.</li>
                    <li>Entrar em contato com o gestor do setor</li>
                </ul>
            """,
            "Opened": "",
            "Approved": "",
            "Denied": "",
        },
        "TI": {
            "Pending": f"""
                <h3>TI ⬇️</h3>
                <ul>
                    <li>Verificar equipamentos</li>
                    <li>Verificar estoque ou reserva</li>
                    <li>Necessidade de compra</li>
                    <li>Lead time médio</li>
                    <li>Softwares necessários: {instance.software_names if instance.software_names else "Nenhum"}</li>
                    <li>Tem PC: {"Sim" if instance.has_pc else "Não"}</li>
                    <li>Precisa Telefone: {"Sim" if instance.needs_phone else "Não"}</li>
                    <li>Precisa Tablet: {"Sim" if instance.needs_tablet else "Não"}</li>
                    <li>Tem posto de trabalho: {"Sim" if instance.has_workstation else "Não"}</li>
                </ul>
            """,
            "Approved": f"""
                <h3>TI ⬇️</h3>
                <ul>
                    <li>Criar e-mail</li>
                    <li>Criar login nos softwares</li>
                    <li>Criar login no ERP</li>
                </ul>
                <h4>Dados:</h4>
                <ul>
                    <li>Nome Completo: {instance.complete_name}</li>
                    {f"<li>Data de início: {formatted_start_date}</li>" if formatted_start_date else ""}
                    <li>Reposição: {"Sim" if instance.is_replacement else "Não"}</li>
                    {f"<li>E-mail substituído: {instance.replaced_email}</li>" if instance.is_replacement else ""}
                </ul>
            """,
            "Opened": "",
            "Denied": "",
        },
    }

    return TEMPLATES
