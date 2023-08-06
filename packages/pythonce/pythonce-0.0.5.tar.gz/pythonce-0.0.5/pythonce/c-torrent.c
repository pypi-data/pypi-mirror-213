#include <stdio.h>
#include <stdlib.h>
#include <libtorrent/session.h>
#include <libtorrent/alert_types.hpp>
#include <libtorrent/torrent_info.hpp>
#include <libtorrent/create_torrent.hpp>

int main() {
    // Criar uma sessão do cliente BitTorrent
    lt::session ses;

    // Configurar as opções do torrent
    lt::settings_pack settings;
    settings.set_int(lt::settings_pack::upload_rate_limit, 500000); // Definir limite de upload
    ses.apply_settings(settings);

    // Adicionar um arquivo ao cliente para criar um torrent
    lt::add_torrent_params torrentParams;
    torrentParams.ti = std::make_shared<lt::torrent_info>("4KShort Film-(1080p60).mp4");
    torrentParams.save_path = "saida_torrent";
    ses.async_add_torrent(torrentParams);

    // Aguardar o término do upload
    while (true) {
        std::vector<lt::alert*> alerts;
        ses.pop_alerts(&alerts);
        for (lt::alert* alert : alerts) {
            // Tratamento de alerta de erro
            if (lt::torrent_error_alert* errorAlert = lt::alert_cast<lt::torrent_error_alert>(alert)) {
                printf("Erro: %s\n", errorAlert->error.message().c_str());
            }

            // Tratamento de alerta de progresso
            if (lt::torrent_checked_alert* checkedAlert = lt::alert_cast<lt::torrent_checked_alert>(alert)) {
                float progress = checkedAlert->progress();
                printf("Progresso: %.2f%%\n", progress * 100);
            }

            // Outros tratamentos de alerta conforme necessário...
        }

        // Verifique se o upload está completo
        if (ses.is_finished()) {
            break;
        }
    }

    // Encerrar a sessão do cliente BitTorrent
    ses.abort();

    return 0;
}
