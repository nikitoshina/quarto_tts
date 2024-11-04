return {{
    Meta = function (meta)
        for _, fmt in ipairs({'html', 'latex',
                              'docx', 'markdown'}) do
            if quarto.doc.is_format(fmt) then
                out_format = fmt
                break
            end
        end
        print(os.getenv("PWD"))
        meta['quarto_doc_params'] = {
            output_directory = quarto.project.output_directory or ".",
            input_file = quarto.doc.input_file or "index.md",
            output_file = quarto.doc.output_file or PANDOC_STATE.output_file or "index.html",
            out_format = out_format or FORMAT
        }
        return meta
    end
}}