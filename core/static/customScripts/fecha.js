$('#personalDataModal').on('shown.bs.modal', function() {
    $('#datetimepicker_fecha_nacimiento').datetimepicker({
      format: 'MM/DD/YYYY', 
      locale: 'es',
      defaultDate: new Date()
    });
  });